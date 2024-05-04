from django.shortcuts import render
from .models import *
from datetime import date
from datetime import datetime
from django.views.generic import View ,ListView, CreateView ,DeleteView, UpdateView ,DetailView,TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from .forms import *
from django.urls import reverse_lazy
from django.contrib.auth.models import Permission 
from django.contrib.auth.models import User
from django.shortcuts import redirect

from django.http import HttpResponse,HttpResponseRedirect
import io



#def index(request):
#	return render(request,'ip/index.html')



class index(View):
	def get(self, request):
		return render(request,'ip/index.html')


class registrar(CreateView):
	form_class = registrar_ip
	template_name = 'ip/registrar-ip.html'
	success_url = reverse_lazy("ip")

	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		return context

	def form_valid(self, form):
		data = form.save(commit=False)
		data.save()
		return super().form_valid(form)


class ip_list(ListView):
	model = registro_ip
	template_name = 'ip/list.html'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['fields'] = registro_ip.objects.all()#Recepcion.objects.all()
		urls = ['eliminar-ip','editar-ip']
		context['urls']=urls
		return context


class ip_delete(DeleteView):
	model = registro_ip
	template_name = 'ip/eliminar-ip.html'
	success_url = reverse_lazy("ip")


class ip_update(UpdateView):
	model = registro_ip
	form_class = registrar_ip
	template_name = 'ip/editar-ip.html'
	success_url = reverse_lazy('ip')