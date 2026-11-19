from django import forms
from django.utils.html import strip_tags
from .models import Paciente,Medico,Cita,Consulta
class PacienteForm(forms.ModelForm):
 class Meta: model=Paciente; fields='__all__'; widgets={'fecha_nacimiento':forms.DateInput(attrs={'type':'date'})}
class CitaForm(forms.ModelForm):
 class Meta: model=Cita; fields=['paciente','medico','fecha_hora','motivo']; widgets={'fecha_hora':forms.DateTimeInput(attrs={'type':'datetime-local'}),'motivo':forms.Textarea()}
 def clean_motivo(self): return strip_tags(self.cleaned_data['motivo']).strip()
 def clean_fecha_hora(self):
  d=self.cleaned_data['fecha_hora']; wd=d.weekday(); h=d.hour
  if wd>5 or (wd<5 and not 8<=h<18) or (wd==5 and not 8<=h<13): raise forms.ValidationError('Atención: L-V 08:00-18:00, sábado 08:00-13:00.')
  return d
class ConsultaForm(forms.ModelForm):
 class Meta: model=Consulta; exclude=['cita','finalizada']
 def clean(self):
  d=super().clean()
  if self.instance.pk and self.instance.finalizada and any(k in self.changed_data for k in ('diagnostico','tratamiento','medicamentos','proxima_cita','referencias')): raise forms.ValidationError('Consulta finalizada: agregue notas, no modifique el registro clínico.')
  return d
