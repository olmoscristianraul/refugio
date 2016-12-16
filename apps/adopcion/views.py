from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, CreateView
from django.core.urlresolvers import reverse_lazy

from app.adopcion.model import Persona, Solicitud
from apps.adopcion.froms import PersonaForm, SolicitudForm

def index_adopcion(request):
	return HttpResponse("soy la pagina principal de adopción")

class SolicitudList(ListView):
	model = Solicitud
	template_name = 'adopcion/solicitud_list.html'

class SolicitudCreate(CreateView):
	model = Solicitud
	template_name = 'adopcion/solicitud_form.html'
	from_class = SolicitudForm
	second_form_class = PersonaForm
	success_url = reverse_lazy('adopcion:solicitud_listar')