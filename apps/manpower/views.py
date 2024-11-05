from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView
from apps.manpower.forms import AsistenciaForm, DescargueForm, PersonalForm, PreliminarForm
from apps.manpower.models import Asistencia, Campania, Descargue, Personal, Preliminar


# ------------------------------------------------------------------------------------>
# view home

class HomeView(TemplateView):
    template_name = "index.html"


class NominaView(TemplateView):
    template_name = "preliminar/tabla_nomina.html"

    def get_context_data(self, **kwargs):
        # Obtén el contexto base llamando al método de la superclase
        context = super().get_context_data(**kwargs)
        
        # Agrega los datos del modelo Preliminar al contexto
        context['nomina_list'] = Preliminar.objects.all()
        
        return context


# ------------------------------------------------------------------------------------>
# view personal


class PersonalList(ListView):
    model = Personal
    template_name = 'personal/personal_list.html'
    context_object_name = 'personal_list'
    queryset = Personal.objects.all()

class PersonalCreate(CreateView):
    model = Personal
    form_class = PersonalForm
    template_name = 'personal/personal_form.html'
    success_url = reverse_lazy('nomina:personal_list')

class PersonalUpdate(UpdateView):
    model = Personal
    form_class = PersonalForm
    template_name = 'personal/personal_form.html'
    success_url = reverse_lazy('nomina:personal_list')    

class PersonalDelete(DeleteView):
    model = Personal
    form_class = PersonalForm
    template_name = 'personal/personal_delete.html'
    success_url = reverse_lazy('nomina:personal_list') 


# ------------------------------------------------------------------------------------>
# view preliminar 


class PreliminarCreate(CreateView):
    model = Preliminar
    form_class = PreliminarForm
    template_name = 'preliminar/preliminar_form.html'
    success_url = reverse_lazy('nomina:nomina_list')

class PreliminarList(ListView):
    model = Preliminar
    template_name = 'preliminar/preliminar_list.html'
    context_object_name = 'preliminar_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        campanias = Campania.objects.filter(estado=True)
        preliminares = Preliminar.objects.all()
        
        preliminares_por_campania = {}  # Cambié el nombre para mayor claridad
        for campania in campanias:
            # Filtra preliminares para la campaña actual
            preliminares_campania = preliminares.filter(campania=campania)

            # Inicializa un diccionario para los cargos de la campaña actual
            cargos_por_campania = {}

            for preliminar in preliminares_campania:
                cargo_nombre = preliminar.cargo

                if cargo_nombre in cargos_por_campania:
                    cargos_por_campania[cargo_nombre]['cantidad'] += 1  # Incrementa el conteo si el cargo ya existe
                else:
                    cargos_por_campania[cargo_nombre] = {
                        'cantidad': 1,
                        'salario_base': preliminar.salario_base,  # Suponiendo que el modelo tiene este campo
                        'vacaciones': preliminar.vacaciones,  # Suponiendo que el modelo tiene este campo
                        'aguinaldo': preliminar.aguinaldo,  # Suponiendo que el modelo tiene este campo
                        'indemnizacion': preliminar.indemnizacion,  # Suponiendo que el modelo tiene este campo
                        'total': preliminar.total_base,  # Suponiendo que el modelo tiene este campo
                    }  # Inicializa los valores correspondientes

            # Asigna el diccionario de cargos a la campaña en el diccionario principal
            preliminares_por_campania[campania] = cargos_por_campania

        context['preliminares'] = preliminares_por_campania
        return context

class PreliminarDetail(DetailView):
    model = Preliminar
    template_name = 'preliminar/preliminar_detail.html'
    queryset = Preliminar.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Datos de asistencia y descargue para la campaña y el personal específicos
        asistencia = Asistencia.objects.filter(campania=self.object.campania, personal=self.object.personal)
        descargue = Descargue.objects.filter(campania=self.object.campania)
        
        # Inicialización de variables para cálculos
        coincidencias, sumatoria_monto, sumatoria_dias = [], 0, 0
        sumatoria_salario_dia, sumatoria_salario_base = 0, 0
        sumatoria_vacaciones, sumatoria_aguinaldo, sumatoria_indemnizacion = 0, 0, 0

        for a in asistencia:
            for d in descargue:
                if a.fecha == d.fecha:
                    # Cuenta de personal con mismo cargo en esa fecha
                    personal_count = Asistencia.objects.filter(
                        campania=self.object.campania,
                        fecha=a.fecha,
                        cargo = self.object.cargo
                    ).count()
                    # Cálculo de valores por día y sumas totales
                    salario_por_dia = (self.object.total / personal_count) * d.monto
                    salario_base = (self.object.sb() / personal_count) * d.monto
                    vacaciones = (self.object.vacaciones()['monto'] / personal_count) * d.monto
                    aguinaldo = (self.object.aguinaldo()['monto'] / personal_count) * d.monto
                    indemnizacion = (self.object.indemnizacion()['monto'] / personal_count) * d.monto

                    # Agregar a sumatorias y coincidencias
                    sumatoria_salario_dia += salario_por_dia
                    sumatoria_salario_base += salario_base
                    sumatoria_vacaciones += vacaciones
                    sumatoria_aguinaldo += aguinaldo
                    sumatoria_indemnizacion += indemnizacion
                    sumatoria_monto += d.monto
                    sumatoria_dias += 1

                    coincidencias.append({
                        'fecha': a.fecha,
                        'persona': a.personal,
                        'campania': a.campania,
                        'monto': d.monto,
                        'cantidad_personal': personal_count,
                        'salario_por_dia': round(salario_por_dia, 2),
                    })
        
        # Agregar datos finales al contexto
        context['coincidencias'] = coincidencias
        context.update({
            'sumatoria_monto': sumatoria_monto,
            'sumatoria_dias': sumatoria_dias,
            'sumatoria_salario_dia': round(sumatoria_salario_dia - ((salario_base + sumatoria_vacaciones) * 0.07), 2),
            'sumatoria_salario_base': round(sumatoria_salario_base, 2),
            'sumatoria_vacaciones': round(sumatoria_vacaciones, 2),
            'sumatoria_aguinaldo': round(sumatoria_aguinaldo, 2),
            'sumatoria_indemnizacion': round(sumatoria_indemnizacion, 2),
            'inss_laboral': round((salario_base + sumatoria_vacaciones) * 0.07, 2),
            'inss_patronal': round((sumatoria_salario_base + sumatoria_vacaciones) * 0.225, 2),
        })
        
        return context

class PreliminarUpdate(UpdateView):
    model = Preliminar
    form_class = PreliminarForm
    template_name = 'preliminar/preliminar_form.html'
    success_url = reverse_lazy('nomina:preliminar_list')    

class PreliminarDelete(DeleteView):
    model = Preliminar
    form_class = PreliminarForm
    template_name = 'preliminar/preliminar_delete.html'
    success_url = reverse_lazy('nomina:preliminar_list')

    
# ------------------------------------------------------------------------------------>
# view asistencia


class AsistenciaList(ListView):
    model = Asistencia
    template_name = 'asistencia/asistencia_list.html'
    context_object_name = 'asistencia_list'
    queryset = Asistencia.objects.all()
    
class AsistenciaCreate(CreateView):
    model = Asistencia
    form_class = AsistenciaForm
    template_name = 'asistencia/asistencia_form.html'
    success_url = reverse_lazy('nomina:asistencia_list')

class AsistenciaUpdate(UpdateView):
    model = Asistencia
    form_class = AsistenciaForm
    template_name = 'asistencia/asistencia_form.html'
    success_url = reverse_lazy('nomina:asistencia_list')    

class AsistenciaDelete(DeleteView):
    model = Asistencia
    form_class = AsistenciaForm
    template_name = 'asistencia/asistencia_delete.html'
    success_url = reverse_lazy('nomina:asistencia_list')
# ------------------------------------------------------------------------------------>
# view carga tonelaje


class DescargueList(ListView):
    model = Descargue
    template_name = 'descargue/descargue_list.html'
    context_object_name = 'descargue_list'
    queryset = Descargue.objects.all()

class DescargueCreate(CreateView):
    model = Descargue
    form_class = DescargueForm
    template_name = 'descargue/descargue_form.html'
    success_url = reverse_lazy('nomina:descargue_list')

class DescargueUpdate(UpdateView):
    model = Descargue
    form_class = DescargueForm
    template_name = 'descargue/descargue_form.html'
    success_url = reverse_lazy('nomina:descargue_list')   

class DescargueDelete(DeleteView):
    model = Descargue
    form_class = DescargueForm
    template_name = 'descargue/descargue_delete.html'
    success_url = reverse_lazy('nomina:descargue_list') 
