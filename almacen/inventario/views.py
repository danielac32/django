from django.shortcuts import render
from .models import *
from datetime import date
from datetime import datetime

from django.views.generic import View ,ListView, CreateView ,DeleteView, UpdateView ,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
# Create your views here.

from .forms import *
from django.urls import reverse_lazy
from django.contrib.auth.models import Permission 
from django.contrib.auth.models import User
from django.shortcuts import redirect

from django.http import HttpResponse,HttpResponseRedirect

from pathlib import Path
from django.conf import settings
from django.contrib import messages
from django.views import View

import xlsxwriter
import io
from django.core.mail import send_mail
from django.contrib import messages



def index(request):
	if request.user.is_authenticated:
		return render(request,'index.html')
	else:
		response = redirect("/accounts/login/")
		return response


class CategoriaCreateView(LoginRequiredMixin,CreateView):
	form_class = Ingresar_Categoria
	template_name = 'categoria.html'
	permission_denied_message = 'No tienes permisos'
	success_url = reverse_lazy("crear-categoria")
	permission_denied_message = 'No tienes permisos'
	permission_required = ['inventario.add_categoria',] 
 
	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		return context

	def form_valid(self, form):
		"""If the form is valid, save the associated model."""
		data = form.save(commit=False)
		data.creator = self.request.user
		data.save()
		return super(CategoriaCreateView, self).form_valid(form)


class ProductoCreateView(LoginRequiredMixin,CreateView):
	form_class = Ingresar_Producto
	template_name = 'ingresar-producto.html'
	permission_denied_message = 'No tienes permisos'
	permission_required = ['inventario.add_producto']
	success_url = reverse_lazy("crear-producto")

 
	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		return context

	def form_valid(self, form):
		"""If the form is valid, save the associated model."""
		data = form.save(commit=False)
		data.creator = self.request.user
		data.save()
		print(data.id)

		mod = Modificacion()
		mod.creator=self.request.user
		mod.tipo="Creado"
		mod.id_producto=data.id
		mod.valor=data.stock
		mod.direccion="Administracion"
		mod.save()
		return super(ProductoCreateView, self).form_valid(form)


class ProductoListView(LoginRequiredMixin,ListView):

	model = Producto
	template_name = 'list.html'
	permission_denied_message = 'No tienes permisos'
	permission_required = ['inventario.view_producto']

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['fields'] = Producto.objects.all()#Recepcion.objects.all()
		urls = ['eliminar-producto','editar-producto','sumar-stock','restar-stock']
		context['urls']=urls
		return context

class ProductoDeleteView(LoginRequiredMixin,DeleteView):
	model = Producto
	template_name = 'eliminar.html'
	permission_denied_message = 'No tienes permisos'
	permission_required = ['inventario.delete_producto']
	success_url = reverse_lazy("lista-producto")


class ProductoUpdateView(LoginRequiredMixin,UpdateView):
	model = Producto
	form_class = Editar_Producto
	template_name = 'editar-producto.html'
	permission_denied_message = 'No tienes permisos'
	permission_required = ['inventario.change_producto']
	success_url = reverse_lazy('lista-producto')




'''item.agregar_stock(313123)
item.restar_stock()'''
def SumarStockUpdateView(request,pk):
	if request.user.is_authenticated:
		context = {}
		if request.method == 'POST':
			form = Actualizar_stock(request.POST)
			if form.is_valid():
				stock = form.cleaned_data['stock']
				item = Producto.objects.filter(id=pk).values_list('stock')
				#print('valor: ',stock,' stock: ',int(item[0][0]),'suma: ',int(stock)+int(item[0][0]))
				Producto.objects.filter(id=pk).update(stock = int(stock)+int(item[0][0]))
				#m = Modificacion.objects.filter(tipo="añadir")
				mod = Modificacion()
				mod.creator=request.user
				mod.tipo="Añadido"
				mod.id_producto=pk
				mod.valor=stock
				mod.direccion="Administracion"
				mod.save()
				return redirect('lista-producto')
		else:
			form = Actualizar_stock()
		context['form']=form
		return render(request,'editar-producto.html',context)
	else:
		return HttpResponse("lista-producto")


def RestarStockUpdateView(request,pk):
	if request.user.is_authenticated:
		context = {}
		if request.method == 'POST':
			form = Actualizar_stock2(request.POST)
			if form.is_valid():
				stock = form.cleaned_data['stock']
				item = Producto.objects.filter(id=pk).values_list('stock')
				#print('valor: ',stock,' stock: ',int(item[0][0]),'suma: ',int(stock)+int(item[0][0]))
				Producto.objects.filter(id=pk).update(stock = int(item[0][0])-int(stock))
				mod = Modificacion()
				mod.creator=request.user
				mod.tipo="Sustraido"
				mod.id_producto=pk
				mod.valor=stock
				mod.direccion=stock = form.cleaned_data['direccion']
				mod.save()
				return redirect('lista-producto')
		else:
			form = Actualizar_stock2()
		context['form']=form
		return render(request,'editar-producto.html',context)
	else:
		return HttpResponse("lista-producto")


'''
class ProductoStockUpdateView(LoginRequiredMixin,UpdateView):
	model = Producto
	form_class = Ingresar_Producto
	template_name = 'editar-producto.html'
	permission_denied_message = 'No tienes permisos'
	success_url = reverse_lazy('lista-producto')
'''


def CreateExcel(request,fecha_inicio,fecha_fin):

	output = io.BytesIO()

	workbook = xlsxwriter.Workbook(output)
	worksheet = workbook.add_worksheet()

    # Get some data to write to the spreadsheet.
	consulta = Producto.objects.filter(created__range=[fecha_inicio,fecha_fin])

	# Write some test data.
	counter = 0	
	counter2  = 0
	titulos = ['Codigo','Nombre','Categoria','Disponible','Observacion','Accion','Cantidad','Fecha','Direccion']


	for key,value in enumerate(titulos):
		worksheet.write(0, key, value)

	for item in consulta:
		counter +=1
		worksheet.write(counter, 0, item.codigo)
		worksheet.write(counter, 1, item.nombre)
		worksheet.write(counter, 2, str(item.categoria))
		worksheet.write(counter, 3, str(item.stock))
		worksheet.write(counter, 4, item.observacion)# Nº de oficio
		print(item.codigo)
		print(item.nombre)
		print(item.categoria)
		print(str(item.stock))
		print(item.observacion)

		fecha = Modificacion.objects.filter(id_producto = item.id)
		for x in fecha:
			counter +=1
			worksheet.write(counter, 5, x.tipo)
			worksheet.write(counter, 6, str(x.valor))
			worksheet.write(counter, 7, str(x.created.strftime("%d/%m/%y")))
			worksheet.write(counter, 8, x.direccion)
			
			print(x.tipo,x.valor,x.created)
			print("*********************")
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
	template_name = "reporte.html"

	def get(self,request,*args,**kwargs):
		form = self.form_class(initial=self.initial)
		return render(request, self.template_name, {"form":form})

	def post(self,request,*args,**kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():
			return CreateExcel(request,form.cleaned_data.get("fecha_inicio"),form.cleaned_data.get("fecha_fin"))
		return render(request, self.template_name, {"form":form})
