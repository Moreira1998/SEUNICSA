from django import forms
from apps.manpower.models import Asistencia, Descargue, Personal, Preliminar

# -------------------------------------------------------->
# Forms preliminar

class PreliminarForm(forms.ModelForm):
    class Meta:
        model = Preliminar 
        fields = '__all__'
        labels = {
            'cargo': 'Cargo',
            'personal': 'Personal',
            'campania': 'Campaña',
            'total': 'Tarifa'
        }
        widgets = {
            'cargo': forms.Select(attrs={'class': 'form-control'}),
            'personal': forms.Select(attrs={'class': 'form-control'}),
            'campania': forms.Select(attrs={'class': 'form-control'}),
            'total': forms.TextInput(attrs={'class': 'form-control'}),
        }

# -------------------------------------------------------->
# Forms asistencia

class PersonalForm(forms.ModelForm):
    class Meta:
        model = Personal 
        fields = '__all__'
        labels = {
            'cedula': 'Cedula',
            'nombre': 'Nombre',
            'inss': 'INSS',
        }
        widgets = {
            'cedula': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'inss': forms.TextInput(attrs={'class': 'form-control'}),
        }


# -------------------------------------------------------->
# Forms asistencia

class AsistenciaForm(forms.ModelForm):
    class Meta:
        model = Asistencia
        fields = '__all__'
        labels = {
            'personal': 'Nombre',
            'cargo': 'Cargo',
            'campania': 'Campaña',
            'fecha': 'Fecha'
        }
        widgets = {
            'personal': forms.Select(attrs={'class': 'form-control'}),
            'cargo': forms.Select(attrs={'class': 'form-control'}),
            'campania': forms.Select(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }


# -------------------------------------------------------->
# Forms asistencia

class DescargueForm(forms.ModelForm):
    class Meta:
        model = Descargue
        fields = '__all__'
        labels = {
            'campania': 'Campaña',
            'fecha': 'Fecha',
            'monto': 'Monto descargue'
        }
        widgets = {
            'campania': forms.Select(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'monto': forms.TextInput(attrs={'class': 'form-control'}),
        }