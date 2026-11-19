from django.urls import path
from . import views
urlpatterns=[path('',views.citas,name='citas'),path('ingresar/',views.login_view,name='login'),path('salir/',views.logout_view,name='logout'),path('agendar/',views.agendar,name='agendar'),path('reportes/',views.reportes,name='reportes'),path('cita/<int:pk>/cancelar/',views.cancelar,name='cancelar'),path('cita/<int:pk>/consulta/',views.consulta,name='consulta'),path('historial/<int:pk>/',views.historial,name='historial')]
