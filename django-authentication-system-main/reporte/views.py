from django.shortcuts import render
from .models import *
from datetime import date
from datetime import datetime
from django.views.generic import View ,ListView, CreateView ,DeleteView, UpdateView ,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from .forms import *
from django.urls import reverse_lazy
from django.contrib.auth.models import Permission 
from django.contrib.auth.models import User
from django.shortcuts import redirect

from django.http import HttpResponse,HttpResponseRedirect
import io



#def index(request):
#	return render(request,'reporte/index.html')
class index(View):
	def get(self, request):
		return render(request,'reporte/index.html')

class registrar_soporte(CreateView):
	form_class = registrar
	template_name = 'reporte/registrar.html'
	success_url = reverse_lazy("index")

	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		return context

	def form_valid(self, form):
		data = form.save(commit=False)
		data.save()
		return super().form_valid(form)


class list(ListView):
	model = reporte_soporte
	template_name = 'reporte/list.html'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['fields'] = reporte_soporte.objects.all()#Recepcion.objects.all()
		urls = ['eliminar','editar']
		context['urls']=urls
		return context