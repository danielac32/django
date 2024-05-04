from django.shortcuts import render ,get_object_or_404
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
#from django.views.generic.edit import FormView
#from django.template.response import TemplateResponse
from django.http import HttpResponse,HttpResponseRedirect
#from django.template import loader
from pathlib import Path
from django.conf import settings
from django.contrib import messages
from django.views import View
import xlsxwriter
import io
from django.core.mail import send_mail

#esta funcion recibe como parametro request 
#comprueba a que grupo pertenece el usuario 
#comprueba que el campo entregado esta en falso y lo coloca a true 
#sino hay usuarios en el grupo da error 
def comprobar_entregado(request):
	group = request.user.groups.all()[0].name
	if group == 'taquilla':
		pass
	else:#si es otro grupo
		entregado = Oficio.objects.filter(usuario=request.user).values_list('entregado')
		for x in entregado:
			print(x[0])
			if bool(x[0]) == False: # si entregado es false 
				Oficio.objects.filter(usuario=request.user).update(entregado = True)
	


#esta funcion por el momento solo cambia el estatus visto a true cuando se descarga el oficio o memo
#deberia descargar el archivo correspondiente
#solo lo hace el usuario
def descargar(request,pk):
	if request.user.is_authenticated:
		group = request.user.groups.all()[0].name
		oficio = get_object_or_404(Oficio,id=pk)
		if group == 'taquilla':
			pass 
		else:
			visto = Oficio.objects.filter(id=pk).values_list('visto')
			if bool(visto[0][0]) == False:#si es falso se coloca en true
				print("visto")
				Oficio.objects.filter(id=pk).update(visto = True)

	return HttpResponseRedirect(f"/media/{oficio.recepcion.imagen}")
	
#esta funcion cambia el estatus devolver 
def devolver(request,pk):
	if request.user.is_authenticated:
		group = request.user.groups.all()[0].name
		if group == 'taquilla':
			pass 
		else:
			devolver = Oficio.objects.filter(id=pk).values_list('devolver')
			if bool(devolver[0][0]) == False:#si es falso se coloca en true
				print("devuelto")
				Oficio.objects.filter(id=pk).update(devolver = True)

	return redirect('list-oficio')


#esta funcion cambia el estatus ejecutado 
def ejecutado(request,pk):
	if request.user.is_authenticated:
		group = request.user.groups.all()[0].name
		if group == 'taquilla':
			pass 
		else:
			ejecutado = Oficio.objects.filter(id=pk).values_list('ejecutado')
			if bool(ejecutado[0][0]) == False:#si es falso se coloca en true
				print("devuelto")
				Oficio.objects.filter(id=pk).update(ejecutado = True)

	return redirect('list-oficio')


def eliminarOficio(request,pk):
	if request.user.is_authenticated:
		group = request.user.groups.all()[0].name
 
		if group == 'taquilla':
			Oficio.objects.filter(id=pk).update(estatus = True)
			messages.success(request, 'Oficio eliminado')
			return redirect('list-oficio')


def eliminarRecepcion(request,pk):
	if request.user.is_authenticated:
		group = request.user.groups.all()[0].name

		if group == 'taquilla':
			Recepcion.objects.filter(pk=pk).update(estatus = True)
			messages.success(request, 'Recepcion eliminada')
			return redirect('list-reception')

class index(LoginRequiredMixin,ListView):
	model = Oficio
	#context_object_name = 'categoria_list'
	template_name = 'index.html'
	permission_denied_message = 'No tienes permisos'

	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		comprobar_entregado(self.request)
		
		
		return context


class RecepcionListView(PermissionRequiredMixin,LoginRequiredMixin,ListView):

	model = Recepcion
	#context_object_name = 'categoria_list'
	template_name = 'crud/list.html'
	permission_denied_message = 'No tienes permisos'


	permission_required = ['app1.view_recepcion']
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		urls = ['eliminarRecepcion','detalle-reception','editar-reception']#3 urls de van en los href
		context['fields'] = Recepcion.objects.filter(estatus=False)#Recepcion.objects.all()
		context['urls'] = urls
		context['quien'] = 'recepcion'#se le indica a la plantilla quien es la clase
		
		return context






class OficioCreate2View(PermissionRequiredMixin,LoginRequiredMixin,CreateView):
	model = Oficio
	form = OficioForm
	form_class = OficioForm3
	template_name = 'crud/create.html'
	permission_denied_message = 'No tienes permisos'
	permission_required = ['app1.add_oficio',]
	success_url = reverse_lazy('create-reception')
 
	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		context['name']='oficio'
		
		return context

	def form_valid(self, form):
		"""If the form is valid, save the associated model."""
		data = form.save(commit=False)
		data.creator = self.request.user
		data.save()
		send_mail(
			"Usted posee una correspondencia",
			"Por favor revise su correspondencia",
			"correspondenciaont@gmail.com",
			f"{data.usuario.email}"
			)
		return super(OficioCreate2View, self).form_valid(form)



class RecepcionCreateView(PermissionRequiredMixin,LoginRequiredMixin,CreateView):
	model = Recepcion
	form_class = RecepcionForm
	context_object_name = 'recepcion'
	template_name = 'crud/create.html'
	permission_denied_message = 'No tienes permisos'
	permission_required = ['app1.add_recepcion',] 


	success_url = reverse_lazy("create-oficio2")

 
	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		context['name']='recepcion'
		return context

	def form_valid(self, form):
		"""If the form is valid, save the associated model."""
		data = form.save(commit=False)
		data.creator = self.request.user
		data.save()
		return super(RecepcionCreateView, self).form_valid(form)

'''
class RecepcionBorrarView(PermissionRequiredMixin,LoginRequiredMixin,DeleteView):
	model = Recepcion
	template_name = 'crud/delete.html'
	permission_denied_message = 'No tienes permisos'
	success_url = reverse_lazy('list-reception')
	permission_required = ['app1.delete_recepcion']

	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		print(self.kwargs.get('pk'))
		print("eliminado")
		Recepcion.objects.filter(pk=self.kwargs.get('pk')).update(estatus = True)
		context['error'] = "eliminado"
		context['urls'] = "list-reception"
		return context
'''

class RecepcionEditarView(PermissionRequiredMixin,LoginRequiredMixin,UpdateView):
	model = Recepcion
	template_name = 'crud/update.html'
	permission_denied_message = 'No tienes permisos'
	permission_required = ['app1.change_recepcion']

	fields = ['mensajero',
                  'asunto',
                  'rif_ci',
                  'oficina']
	success_url = reverse_lazy('list-reception')




class RecepcionDetalleView(PermissionRequiredMixin,LoginRequiredMixin,DetailView):
	model = Recepcion
	#form_class = RecepcionForm
	template_name = 'crud/detail.html'
	permission_denied_message = 'No tienes permisos'
	permission_required = ['app1.view_recepcion',] 
	success_url = reverse_lazy('list-reception')

	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		#context['fields'] =Recepcion.objects.filter(pk=self.kwargs.get('pk'))
		#context['now'] = datetime.datetime.now()
		context['quien']='recepcion'
		return context


######################################################################3



class OficioListView(PermissionRequiredMixin,LoginRequiredMixin,ListView):
	model = Oficio
	#context_object_name = 'categoria_list'
	template_name = 'crud/list.html'
	permission_denied_message = 'No tienes permisos'
	permission_required = ['app1.view_oficio']

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		urls = ['eliminarOficio','detalle-oficio','editar-oficio','observacion']
		group = self.request.user.groups.all()[0].name# obtenemos el grupo al que pertenece 
		#print(self.request.user)

		if group == 'taquilla':
			context['fields'] = Oficio.objects.filter(estatus=False)
		else:
			context['fields'] = Oficio.objects.filter(usuario=self.request.user,devolver=False,estatus=False)
		'''
		if group == 'usuario':#si es usuario obtenemos el id usando el nombre usando la tabla user 
			#id = User.objects.filter(username=self.request.user).values_list('id')
			#obtenemos los oficios asociados al el id obtenido
			context['fields'] = Oficio.objects.filter(usuario=self.request.user,devolver=False,estatus=False)
		else:	
			context['fields'] = Oficio.objects.filter(estatus=False)'''
		
		context['urls'] = urls
		context['quien'] = 'oficio'
		comprobar_entregado(self.request)##cambiar estatus a entregado
		#print("------",date.today(),self.request.user.email)
		return context


class OficioCreateView(PermissionRequiredMixin,LoginRequiredMixin,CreateView):
	model = Oficio
	form_class = OficioForm2
	template_name = 'crud/create.html'
	permission_denied_message = 'No tienes permisos'
	permission_required = ['app1.add_oficio',]
	success_url = reverse_lazy('create-oficio')
 
	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		context['name']='oficio'
		return context

	def form_valid(self, form):
		"""If the form is valid, save the associated model."""
		data = form.save(commit=False)
		data.creator = self.request.user
		data.save()
		send_mail(
			"Usted posee una correspondencia",
			"Por favor revise su correspondencia",
			"correspondenciaont@gmail.com",
			f"{data.usuario.email}"
			)
		return super(OficioCreateView, self).form_valid(form)
       
''''
class OficioBorrarView(PermissionRequiredMixin,LoginRequiredMixin,DeleteView):
	model = Oficio
	template_name = 'crud/delete.html'
	permission_denied_message = 'No tienes permisos'
	success_url = reverse_lazy('list-reception')
	permission_required = ['app1.delete_oficio']

	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		print(self.kwargs.get('pk'))
		status = Oficio.objects.filter(pk=self.kwargs.get('pk')).values_list('entregado','estatus','devolver')[0]
		for x in status:
			print(x)
		if status[2] == True: # si el oficio esta devuelto, entonces cambia su estatus a true
			print("eliminado")
			#Oficio.objects.filter(pk=self.kwargs.get('pk')).update(estatus = True)
			context['error'] = "eliminado"
		elif status[0] == True and status[2]==False:# si esta entregado pero no devuelto no lo puede eliminar
			context['error'] = "entregado"
		elif status[0] == False and status[2]== False:
			print("eliminado")
			#Oficio.objects.filter(pk=self.kwargs.get('pk')).update(estatus = True)
			context['error'] = "eliminado"
		return context
'''

class OficioEditarView(PermissionRequiredMixin,LoginRequiredMixin,UpdateView):
	model = Oficio
	form_class = OficioForm
	template_name = 'crud/update.html'
	permission_denied_message = 'No tienes permisos'
	permission_required = ['app1.change_oficio']
	success_url = reverse_lazy('index')
"""
	def get_form_class(self):
		if self.request.user.groups.asdlnkjasdklasdajlskd == "usuario"
			self.form_class = UsuarioEditarForm
		else if self.request.user.groups.asdlnkjasdklasdajlskd == "usuario"
			self.form_class = TaquillaEditarForm
		return self.form_class
"""


class OficioDetalleView(PermissionRequiredMixin,LoginRequiredMixin,DetailView):
	model = Oficio
	template_name = 'crud/detail.html'
	permission_denied_message = 'No tienes permisos'
	success_url = reverse_lazy('list-oficio')
	permission_required = ['app1.view_oficio',]

	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		#context['fields'] = Oficio.objects.filter(pk=self.kwargs.get('pk'))
		#context['now'] = datetime.datetime.now()
		context['quien']='oficio'
		context['url_view']=context['object'].recepcion.imagen
		#print(context)
		#print(self.request.user)
		#print(context['object'].recepcion.imagen)
		#print(Path(__file__).resolve().parent.parent)
		#print(Oficio.objects.filter(recepcion=self.request.user).values_list('imagen'))


		#context['url_image']= Oficio.objects.filter(usuario=self.request.user).values_list('imagen')
		#print(context['url_image'])
		return context

class OficioObservacionView(PermissionRequiredMixin,LoginRequiredMixin,UpdateView):
	model = Oficio
	form = OficioForm
	#form_class = OficioForm
	template_name = 'detalles.html'
	permission_denied_message = 'No tienes permisos'
	fields = ['observacion']
	#form_class = Observacion
	permission_required = ['app1.change_oficio']
	success_url = reverse_lazy('index')



 


class OficioDevueltoList(PermissionRequiredMixin,LoginRequiredMixin,ListView):
	form_class = OficioForm
	model = Oficio
	#context_object_name = 'categoria_list'
	template_name = 'devuelto.html'
	permission_denied_message = 'No tienes permisos'
	permission_required = ['app1.view_oficio']

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		urls = ['eliminarOficio','detalle-oficio','editar-oficio','observacion']
		context['fields'] = Oficio.objects.filter(devolver=True)
		
		context['urls'] = urls
		return context


def CreateExcel(request,fecha_inicio,fecha_fin):

	output = io.BytesIO()

	workbook = xlsxwriter.Workbook(output)
	worksheet = workbook.add_worksheet()

    # Get some data to write to the spreadsheet.
	consulta = Recepcion.objects.filter(fecha__range=[fecha_inicio,fecha_fin]).exclude(estatus=True)

	# Write some test data.
	counter = 0	
	titulos = ['Remitente','Asunto','Correlativo','Fecha','Nº de Oficio','Direccion']

	for key,value in enumerate(titulos):
		worksheet.write(0, key, value)

	for item in consulta:
		counter +=1
		#worksheet.write(counter, 0, item.persona)
		#worksheet.write(counter, 1, item.telefono)
		worksheet.write(counter, 0, item.mensajero)
		worksheet.write(counter, 1, item.asunto)
		worksheet.write(counter, 2, item.correlativo)
		worksheet.write(counter, 3, str(item.fecha))
		worksheet.write(counter, 4, item.rif_ci)# Nº de oficio
		worksheet.write(counter, 5, item.oficina.oficina)
		#worksheet.write(counter, 8, item.estatus)

	# Close the workbook before sending the data.
	workbook.close()

	# Rewind the buffer.
	output.seek(0)

	# Set up the Http response.
	filename = 'reporte.xlsx'
	response = HttpResponse(
		output,
		content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
	)
	response['Content-Disposition'] = 'attachment; filename=%s' % filename

	return response


class ExcelReport(View):
	form_class = ReportForm
	initial = {"key":"value"}
	template_name = "formulario.html"

	def get(self,request,*args,**kwargs):
		form = self.form_class(initial=self.initial)
		return render(request, self.template_name, {"form":form})

	def post(self,request,*args,**kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():
			return CreateExcel(request,form.cleaned_data.get("fecha_inicio"),form.cleaned_data.get("fecha_fin"))
		return render(request, self.template_name, {"form":form})


class reset_password(View):
	form_class = rp
	initial = {"key":"value"}
	template_name = "nueva_contraseña.html"

	def get(self,request,*args,**kwargs):
		form = self.form_class(initial=self.initial)
		return render(request, self.template_name, {"form":form})

	def post(self,request,*args,**kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():
			correo= form.cleaned_data.get("correo")
			nueva_clave=form.cleaned_data.get("nueva_clave")
			user = user_form.save()

			
			existe = User.objects.filter(email=correo).values_list("password")
			if existe:
				print("ok en proceso",correo,nueva_clave,existe)


			#Oficio.objects.filter(usuario=request.user).update(entregado = True)
			

			

		return render(request, self.template_name, {"form":form})