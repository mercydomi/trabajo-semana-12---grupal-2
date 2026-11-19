from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
class Paciente(models.Model):
 dni=models.CharField(max_length=8,unique=True,validators=[RegexValidator(r'^\d{8}$','DNI debe tener 8 dígitos')]); nombres=models.CharField(max_length=100); apellidos=models.CharField(max_length=100); fecha_nacimiento=models.DateField(); tipo=models.CharField(max_length=10,choices=[('estudiante','Estudiante'),('docente','Docente')]); codigo_uncp=models.CharField(max_length=20,unique=True); alergias=models.TextField(blank=True); correo=models.EmailField()
 @property
 def edad(self): from django.utils import timezone; return (timezone.localdate()-self.fecha_nacimiento).days//365
 def clean(self):
  if not self.correo.endswith('@uncp.edu.pe'): raise ValidationError('Use correo institucional UNCP.')
 def __str__(self): return f'{self.dni} - {self.nombres} {self.apellidos}'
class Medico(models.Model):
 usuario=models.OneToOneField(User,on_delete=models.CASCADE); cmp=models.CharField(max_length=12,unique=True,validators=[RegexValidator(r'^CMP\d{5,8}$','CMP inválido')]); especialidad=models.CharField(max_length=80); horario=models.CharField(max_length=100,default='L-V 08:00-18:00'); consultorio=models.CharField(max_length=40)
 def __str__(self): return f'{self.usuario.get_full_name()} - {self.especialidad}'
class Cita(models.Model):
 paciente=models.ForeignKey(Paciente,on_delete=models.PROTECT); medico=models.ForeignKey(Medico,on_delete=models.PROTECT); fecha_hora=models.DateTimeField(); motivo=models.TextField(); estado=models.CharField(max_length=12,choices=[('pendiente','Pendiente'),('cancelada','Cancelada'),('completada','Completada')],default='pendiente')
 def clean(self):
  if len(self.motivo.strip())<20: raise ValidationError('El motivo requiere al menos 20 caracteres.')
  if not self.fecha_hora or not self.medico_id or not self.paciente_id: return
  if Cita.objects.filter(medico=self.medico,fecha_hora=self.fecha_hora).exclude(pk=self.pk).exists(): raise ValidationError('Horario ocupado para este médico.')
  if Cita.objects.filter(paciente=self.paciente,fecha_hora__date=self.fecha_hora.date()).exclude(pk=self.pk).count()>=2: raise ValidationError('Máximo dos citas por día.')
class Consulta(models.Model):
 cita=models.OneToOneField(Cita,on_delete=models.PROTECT); diagnostico=models.TextField(); tratamiento=models.TextField(); medicamentos=models.TextField(blank=True); proxima_cita=models.DateField(null=True,blank=True); referencias=models.TextField(blank=True); notas_adicionales=models.TextField(blank=True); finalizada=models.BooleanField(default=True)
class AuditoriaClinica(models.Model):
 usuario=models.ForeignKey(User,null=True,on_delete=models.SET_NULL); recurso=models.CharField(max_length=200); fecha=models.DateTimeField(auto_now_add=True); ip=models.GenericIPAddressField(null=True); resultado=models.CharField(max_length=20,default='permitido')
 class Meta: ordering=['-fecha']

# Create your models here.
