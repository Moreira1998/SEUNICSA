from django.urls import path
from apps.manpower.views import AsistenciaDelete, AsistenciaUpdate, DescargueCreate, DescargueDelete, DescargueUpdate, HomeView, PersonalCreate, PersonalDelete, PersonalList, PersonalUpdate, PreliminarCreate, PreliminarDelete, PreliminarDetail, PreliminarList, AsistenciaList, AsistenciaCreate, DescargueList, NominaView, PreliminarUpdate
from apps.manpower.report import export_preliminar_excel
from django.contrib.auth.decorators import login_required

app_name = 'nomina'

urlpatterns = [
    path('', login_required(HomeView.as_view()), name='inicio'),
    path('nomina', login_required(NominaView.as_view()), name='nomina_list'),
    # Personal
    path('personalList', login_required(PersonalList.as_view()), name='personal_list'),
    path('personalCreate', login_required(PersonalCreate.as_view()), name='personal_create'),
    path('personalUpdate/<str:pk>/', login_required(PersonalUpdate.as_view()), name='personal_update'),
    path('personalDelete/<str:pk>/', login_required(PersonalDelete.as_view()), name='personal_delete'),
    # Preliminar
    path('preliminarList', login_required(PreliminarList.as_view()), name='preliminar_list'),
    path('preliminarCreate', login_required(PreliminarCreate.as_view()), name='preliminar_create'),
    # Nomina
    path('nomina/<int:pk>/', login_required(PreliminarDetail.as_view()), name='nomina_detail'),
    path('nominaUpdate/<int:pk>/', login_required(PreliminarUpdate.as_view()), name='nomina_update'),
    path('nominaDelete/<int:pk>/', login_required(PreliminarDelete.as_view()), name='nomina_delete'),
    # Asistencia
    path('asistenciaList', login_required(AsistenciaList.as_view()), name='asistencia_list'),
    path('asistenciaCreate', login_required(AsistenciaCreate.as_view()), name='asistencia_create'),
    path('asistenciaUpdate/<int:pk>/', login_required(AsistenciaUpdate.as_view()), name='asistencia_update'),
    path('asistenciaDelete/<int:pk>/', login_required(AsistenciaDelete.as_view()), name='asistencia_delete'),
    # Descargue
    path('descargueList', login_required(DescargueList.as_view()), name='descargue_list'),
    path('descargueCreate', login_required(DescargueCreate.as_view()), name='descargue_create'),
    path('descargueUpdate/<int:pk>/', login_required(DescargueUpdate.as_view()), name='descargue_update'),
    path('descargueDelete/<int:pk>/', login_required(DescargueDelete.as_view()), name='descargue_delete'),
    # Reporte
    path("export-preliminar/<int:pk>", login_required(export_preliminar_excel), name="export_preliminar"),

    
]