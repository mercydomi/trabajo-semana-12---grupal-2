from django.test import TestCase
from django.contrib.auth.models import User,Group
from django.urls import reverse
from datetime import datetime, timezone as dt_timezone
from .models import Paciente,Medico,Cita
from .forms import CitaForm
from .models import AuditoriaClinica
from django.utils import timezone
class ClinicaTests(TestCase):
 def setUp(self):
  u=User.objects.create_user('medico',password='Demo2026!');self.m=Medico.objects.create(usuario=u,cmp='CMP12345',especialidad='General',consultorio='1');self.p=Paciente.objects.create(dni='12345678',nombres='Ana',apellidos='Demo',fecha_nacimiento='2000-01-01',tipo='estudiante',codigo_uncp='U1',correo='ana@uncp.edu.pe')
 def test_login(self): self.assertTrue(self.client.login(username='medico',password='Demo2026!'))
 def test_motivo_corto(self):
  c=Cita(paciente=self.p,medico=self.m,fecha_hora=datetime(2027,1,4,9),motivo='corto')
  with self.assertRaises(Exception):c.full_clean()
 def test_cita_duplicada(self):
  dt=datetime(2027,1,4,9);Cita.objects.create(paciente=self.p,medico=self.m,fecha_hora=dt,motivo='Motivo de consulta suficientemente detallado.')
  x=Cita(paciente=self.p,medico=self.m,fecha_hora=dt,motivo='Motivo de consulta suficientemente detallado.')
  with self.assertRaises(Exception):x.full_clean()
 def test_horario_invalido_formulario(self):
  f=CitaForm({'paciente':self.p.pk,'medico':self.m.pk,'fecha_hora':'2027-01-03T09:00','motivo':'Motivo de consulta suficientemente detallado.'})
  self.assertFalse(f.is_valid())
 def test_historial_requiere_login(self): self.assertEqual(self.client.get(reverse('historial',args=[self.p.pk])).status_code,302)
 def test_auditoria_historial(self):
  self.client.login(username='medico',password='Demo2026!');self.client.get(reverse('historial',args=[self.p.pk]));self.assertEqual(AuditoriaClinica.objects.count(),1)
 def test_reporte_denegado_sin_admin(self):
  self.client.login(username='medico',password='Demo2026!');self.assertIn(self.client.get(reverse('reportes')).status_code,(302,403))
 def test_hora_mostrada_en_lima(self):
  # Una cita almacenada en UTC se convierte a la hora local activa (UTC-5).
  utc=timezone.make_aware(datetime(2027,1,4,14),dt_timezone.utc)
  self.assertEqual(timezone.localtime(utc).hour,9)
 def test_login_template_responde_200(self):
  response=self.client.get(reverse('login'))
  self.assertEqual(response.status_code,200)
  self.assertTemplateUsed(response,'clinica/login.html')
  self.assertContains(response,"clinica.css")
 def test_agenda_template_responde_200(self):
  self.client.login(username='medico',password='Demo2026!')
  response=self.client.get(reverse('citas'))
  self.assertEqual(response.status_code,200)
  self.assertTemplateUsed(response,'clinica/citas.html')
 def test_reportes_template_admin_responde_200(self):
  admin=User.objects.create_user('admin',password='Demo2026!')
  group,_=Group.objects.get_or_create(name='Administrador');admin.groups.add(group)
  self.client.login(username='admin',password='Demo2026!')
  response=self.client.get(reverse('reportes'))
  self.assertEqual(response.status_code,200)
  self.assertTemplateUsed(response,'clinica/reportes.html')

# Create your tests here.
