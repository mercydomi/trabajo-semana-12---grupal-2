from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import Cita,Paciente,Consulta,Medico
from .forms import CitaForm,ConsultaForm,PacienteForm
def role(u,*names): return u.is_superuser or u.groups.filter(name__in=names).exists()
def login_view(request):
 if request.method=='POST':
  u=authenticate(request,username=request.POST.get('username'),password=request.POST.get('password'))
  if u: login(request,u);return redirect('citas')
  messages.error(request,'Credenciales inválidas.')
 return render(request,'clinica/login.html')
def logout_view(request):
 if request.method=='POST': logout(request)
 return redirect('login')
@login_required
def citas(request):
 qs=Cita.objects.select_related('paciente','medico')
 if role(request.user,'Paciente'): qs=qs.filter(paciente__correo=request.user.email)
 return render(request,'clinica/citas.html',{'citas':qs})
@login_required
@user_passes_test(lambda u:role(u,'Administrador','Recepcionista'))
def agendar(request):
 f=CitaForm(request.POST or None)
 if request.method=='POST' and f.is_valid(): f.save();messages.success(request,'Cita registrada.');return redirect('citas')
 return render(request,'clinica/form.html',{'form':f,'title':'Agendar cita'})
@login_required
def cancelar(request,pk):
 c=get_object_or_404(Cita,pk=pk)
 if not(role(request.user,'Administrador','Recepcionista') or c.paciente.correo==request.user.email): return redirect('citas')
 if request.method=='POST': c.estado='cancelada';c.save();return redirect('citas')
 return render(request,'clinica/confirm.html',{'obj':c,'action':'cancelar'})
@login_required
@user_passes_test(lambda u:role(u,'Medico','Administrador'))
def consulta(request,pk):
 c=get_object_or_404(Cita,pk=pk); obj=getattr(c,'consulta',None);f=ConsultaForm(request.POST or None,instance=obj)
 if request.method=='POST' and f.is_valid(): x=f.save(commit=False);x.cita=c;x.save();c.estado='completada';c.save();return redirect('historial',c.paciente_id)
 return render(request,'clinica/form.html',{'form':f,'title':'Consulta médica'})
@login_required
def historial(request,pk):
 p=get_object_or_404(Paciente,pk=pk)
 autorizado=role(request.user,'Administrador') or p.correo==request.user.email
 if role(request.user,'Medico') and hasattr(request.user,'medico'): autorizado=Cita.objects.filter(paciente=p,medico=request.user.medico).exists()
 if not autorizado: return redirect('citas')
 return render(request,'clinica/historial.html',{'paciente':p,'consultas':Consulta.objects.filter(cita__paciente=p).select_related('cita')})
@login_required
@user_passes_test(lambda u:role(u,'Administrador'))
def reportes(request):
 from django.db.models import Count
 return render(request,'clinica/reportes.html',{'especialidades':Cita.objects.values('medico__especialidad').annotate(total=Count('id')).order_by('-total'),'medicos':Medico.objects.annotate(total=Count('cita')).order_by('-total')[:8],'pacientes':Paciente.objects.annotate(total=Count('cita')).order_by('-total')[:10]})

# Create your views here.
