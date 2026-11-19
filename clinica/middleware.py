from .models import Cita,AuditoriaClinica
class ClinicalAuditMiddleware:
 def __init__(self,response): self.response=response
 def __call__(self,request):
  r=self.response(request)
  if request.user.is_authenticated and '/historial/' in request.path:
   request.session['ultimo_acceso_historial']=request.path
   AuditoriaClinica.objects.create(usuario=request.user,recurso=request.path,ip=request.META.get('REMOTE_ADDR'),resultado='permitido' if r.status_code==200 else 'denegado')
  if request.user.is_authenticated and hasattr(request.user,'medico'):
   request.session['citas_pendientes']=Cita.objects.filter(medico=request.user.medico,estado='pendiente').count()
  return r
