from django.conf.urls import  url

from apps.adopcion.views import index_adopcion, SolicitudList

urlpatterns = [
    url(r'^index$', index_adopcion),
    url(r'^solicitud/listar$', Solicitud.as_view(), name='solicitud_listar'),

]