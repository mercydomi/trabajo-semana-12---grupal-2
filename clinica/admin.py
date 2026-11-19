from django.contrib import admin
from .models import *
@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
 list_display=('fecha_hora','paciente','medico','estado');list_filter=('estado','medico__especialidad');search_fields=('paciente__dni','paciente__nombres');actions=['completar']
 @admin.action(description='Marcar completadas')
 def completar(self,r,q):q.update(estado='completada')
admin.site.register([Paciente,Medico,Consulta,AuditoriaClinica])
