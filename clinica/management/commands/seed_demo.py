from django.core.management.base import BaseCommand
from django.contrib.auth.models import User,Group
from django.utils import timezone
from datetime import timedelta
from clinica.models import Medico,Paciente,Cita
class Command(BaseCommand):
 def add_arguments(self,parser): parser.add_argument('--repair-demo-hours',action='store_true',help='Reubica solo las citas demo identificables creadas con el horario UTC anterior.')
 def handle(self,*a,**k):
  gs={x:Group.objects.get_or_create(name=x)[0] for x in ('Administrador','Medico','Recepcionista','Paciente')}
  admin,_=User.objects.get_or_create(username='admin_med');admin.set_password('Demo2026!');admin.save();admin.groups.set([gs['Administrador']])
  med=[]
  for i in range(8):
   u,_=User.objects.get_or_create(username=f'medico{i+1}',defaults={'first_name':f'Médico {i+1}'});u.set_password('Demo2026!');u.save();u.groups.set([gs['Medico']]);med.append(Medico.objects.get_or_create(usuario=u,defaults={'cmp':f'CMP{10000+i}','especialidad':['Medicina','Odontología','Psicología','Nutrición'][i%4],'consultorio':str(i+1)})[0])
  ps=[]
  for i in range(15): ps.append(Paciente.objects.get_or_create(dni=f'{10000000+i}',defaults={'nombres':f'Paciente {i+1}','apellidos':'Demo','fecha_nacimiento':'2000-01-01','tipo':'estudiante','codigo_uncp':f'U{i+1}','correo':f'paciente{i+1}@uncp.edu.pe'})[0])
  # Hora local de Lima: al guardarse se convierte a UTC y al renderizar vuelve a Lima.
  base=timezone.localtime().replace(hour=9,minute=0,second=0,microsecond=0)
  for i in range(30):
   # Lunes, con bloques 09:00–12:00; evita domingos y horas fuera de atención.
   fecha=base+timedelta(days=(7-base.weekday())%7+(i//8)*7,hours=i%4)
   Cita.objects.get_or_create(paciente=ps[i%15],medico=med[i%8],fecha_hora=fecha,defaults={'motivo':'Consulta ficticia para demostración académica.'})
  if k['repair_demo_hours']:
   demos=Cita.objects.filter(paciente__dni__startswith='100000',motivo='Consulta ficticia para demostración académica.').select_related('paciente','medico').order_by('pk')
   for i,c in enumerate(demos):
    c.fecha_hora=base+timedelta(days=(7-base.weekday())%7+(i//8)*7,hours=i%4); c.save(update_fields=['fecha_hora'])
   self.stdout.write(f'Reparadas {demos.count()} citas demo identificables a hora local Lima.')
  self.stdout.write('Demo: 8 médicos, 15 pacientes, 30 citas. Clave Demo2026!')
