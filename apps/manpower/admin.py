from django.contrib import admin
from apps.manpower.models import Campania, Cargo, Personal, Preliminar, Asistencia, Descargue

# Register your models here.
admin.site.register(Personal)
admin.site.register(Cargo)
admin.site.register(Campania)
admin.site.register(Preliminar)
admin.site.register(Asistencia)
admin.site.register(Descargue)