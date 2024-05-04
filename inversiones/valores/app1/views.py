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



'''
class index(LoginRequiredMixin,ListView):
	model = Barra
	template_name = 'index.html'
	permission_denied_message = 'No tienes permisos'
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		return context


class BarraCreate(PermissionRequiredMixin,LoginRequiredMixin,CreateView):
	model = Barra
	form_class = BarraForm
	template_name = 'crud/create.html'
	permission_denied_message = 'No tienes permisos'
	permission_required = ['app1.add_barra',]
	success_url = reverse_lazy('insert')

	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		context['view']='create_barra'
		return context

	def form_valid(self, form):
		"""If the form is valid, save the associated model."""
		data = form.save(commit=False)
		data.creator = self.request.user
		data.save()
		return super(BarraCreate, self).form_valid(form)


class CalculoBarraCreate(PermissionRequiredMixin,LoginRequiredMixin,CreateView):
	model = calculo_barra
	form_class = CalculoBarraForm
	template_name = 'crud/create.html'
	permission_denied_message = 'No tienes permisos'
	permission_required = ['app1.add_calculo_barra',]
	success_url = reverse_lazy('calcular-barra')


	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		context['view']='calculo_barra'
		return context

	def form_valid(self, form):
		"""If the form is valid, save the associated model."""
		data = form.save(commit=False)
		data.creator = self.request.user
		data.save()
		return super(CalculoBarraCreate, self).form_valid(form)


class CalculoTestigoCreate(PermissionRequiredMixin,LoginRequiredMixin,CreateView):
	model = claculo_testigo
	form_class = CalculoTestigoForm
	template_name = 'crud/create.html'
	permission_denied_message = 'No tienes permisos'
	permission_required = ['app1.add_calculo_testigo',]
	success_url = reverse_lazy('calcular-testigo')


	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		context['view']='calculo_testigo'
		return context

	def form_valid(self, form):
		"""If the form is valid, save the associated model."""
		data = form.save(commit=False)
		data.creator = self.request.user
		data.save()
		return super(CalculoTestigoCreate, self).form_valid(form)
'''
#######################################################################################




def index(request):
	if request.user.is_authenticated:
		return render(request,'index.html')
	else:
		return redirect("login")


def consultar2(request):
	if request.user.is_authenticated:
		return render(request,'item_consultar.html')
	else:
		return redirect("login")


def ingresar_barra(request):
	if request.user.is_authenticated:
		context = {}

		if request.method == 'POST':
			form = BarraForm(request.POST)
			if form.is_valid():
				data = form.save(commit=False)
				buscar_barra = Barra.objects.filter(Cod_barra=data.Cod_barra).values_list('Cod_barra')
				if buscar_barra:
					print('la barra ya existe')
					messages.error(request, 'La Barra ya existe')

				data.creator = request.user
				data.save()

				return redirect('ingresar')
		else:
			form = BarraForm()
		context['form']=form
		return render(request,'ingresar-barra.html',context)

	else:
		return HttpResponse("index")





def CreateExcel(request,fecha_inicio,fecha_fin):
	output = io.BytesIO()

	workbook = xlsxwriter.Workbook(output)
	worksheet = workbook.add_worksheet()


	counter = 0	
	titulos = ['Num operacion','Derechante','Estatus','Complejo','Empresa','Cod barra','Peso bruto','Num guia','Num caja','Fecha Certificado','Peso Final','Fecha Fixing','Fixing','Fecha TDC','TDC','BS','USD','Peso Final','Fecha Fixing','Fixing','Fecha TDC','TDC','BS','USD']
	
	for key,value in enumerate(titulos):
		if key < 8 :
			cell_format = workbook.add_format({'bold': True , 'font_color': 'red'})
		if key > 8 and key <16:
			cell_format = workbook.add_format({'bold': True , 'font_color': 'blue'})
		if key > 16 and key <23:
			cell_format = workbook.add_format({'bold': True , 'font_color': 'green'})

		worksheet.write(0, key, value,cell_format)

	consulta = Barra.objects.filter(created__range=[fecha_inicio,fecha_fin])
	for item in consulta:
		counter +=1
		cell_format = workbook.add_format({'bold': True , 'font_color': 'red'})
		worksheet.write(counter, 0, item.num_operacion,cell_format)
		worksheet.write(counter, 1, str(item.Derechante),cell_format)
		worksheet.write(counter, 2, str(item.Estatus),cell_format)
		worksheet.write(counter, 3, str(item.Complejo),cell_format)
		worksheet.write(counter, 4, str(item.Empresa),cell_format)
		worksheet.write(counter, 5, item.Cod_barra,cell_format)
		worksheet.write(counter, 6, item.peso_bruto,cell_format)
		worksheet.write(counter, 7, str(item.Num_guia_onafin),cell_format)
		worksheet.write(counter, 8, item.num_caja,cell_format)


		consulta2 = calculo_barra.objects.filter(Barra=item.id)

		if(consulta2):
			for item2 in consulta2:
				cell_format = workbook.add_format({'bold': True , 'font_color': 'blue'})
				worksheet.write(counter, 9,str(item2.Fecha_certificado),cell_format)
				worksheet.write(counter, 10,item2.Ley,cell_format)
				worksheet.write(counter, 11,item2.Peso_final,cell_format)#kg
				worksheet.write(counter, 11,str(item2.Fecha_fixing),cell_format)
				worksheet.write(counter, 12,item2.Fixing,cell_format)
				worksheet.write(counter, 13,str(item2.Fecha_tdc),cell_format)
				worksheet.write(counter, 14,item2.TDC,cell_format)
				worksheet.write(counter, 15,item2.BS,cell_format)
				worksheet.write(counter, 16,item2.USD,cell_format)


		consulta3 = claculo_testigo.objects.filter(Barra=item.id)
		if(consulta3):
			for item3 in consulta3:
				cell_format = workbook.add_format({'bold': True , 'font_color': 'green'})

				worksheet.write(counter, 17,item3.Peso_final,cell_format)#kg
				worksheet.write(counter, 18,str(item3.Fecha_fixing),cell_format)
				worksheet.write(counter, 19,item3.Fixing,cell_format)
				worksheet.write(counter, 20,str(item3.Fecha_tdc),cell_format)
				worksheet.write(counter, 21,item3.TDC,cell_format)
				worksheet.write(counter, 22,item3.BS,cell_format)
				worksheet.write(counter, 23,item3.USD,cell_format)


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


 

def CreateExcel2(request,Cod_barra):
	output = io.BytesIO()

	workbook = xlsxwriter.Workbook(output)
	worksheet = workbook.add_worksheet()


	counter = 0	
	titulos = ['Num operacion','Derechante','Estatus','Complejo','Empresa','Cod barra','Peso bruto','Num guia','Num caja','Fecha Certificado','Peso Final','Fecha Fixing','Fixing','Fecha TDC','TDC','BS','USD','Peso Final','Fecha Fixing','Fixing','Fecha TDC','TDC','BS','USD']
	
	for key,value in enumerate(titulos):
		if key < 8 :
			cell_format = workbook.add_format({'bold': True , 'font_color': 'red'})
		if key > 8 and key <16:
			cell_format = workbook.add_format({'bold': True , 'font_color': 'blue'})
		if key > 16 and key <23:
			cell_format = workbook.add_format({'bold': True , 'font_color': 'green'})

		worksheet.write(0, key, value,cell_format)

	consulta = Barra.objects.filter(Cod_barra=Cod_barra)
	for item in consulta:
		counter +=1
		cell_format = workbook.add_format({'bold': True , 'font_color': 'red'})
		worksheet.write(counter, 0, item.num_operacion,cell_format)
		worksheet.write(counter, 1, str(item.Derechante),cell_format)
		worksheet.write(counter, 2, str(item.Estatus),cell_format)
		worksheet.write(counter, 3, str(item.Complejo),cell_format)
		worksheet.write(counter, 4, str(item.Empresa),cell_format)
		worksheet.write(counter, 5, item.Cod_barra,cell_format)
		worksheet.write(counter, 6, item.peso_bruto,cell_format)
		worksheet.write(counter, 7, str(item.Num_guia_onafin),cell_format)
		worksheet.write(counter, 8, item.num_caja,cell_format)


		consulta2 = calculo_barra.objects.filter(Barra=item.id)

		if(consulta2):
			for item2 in consulta2:
				cell_format = workbook.add_format({'bold': True , 'font_color': 'blue'})
				worksheet.write(counter, 9,str(item2.Fecha_certificado),cell_format)
				worksheet.write(counter, 10,item2.Ley,cell_format)
				worksheet.write(counter, 11,item2.Peso_final,cell_format)#kg
				worksheet.write(counter, 11,str(item2.Fecha_fixing),cell_format)
				worksheet.write(counter, 12,item2.Fixing,cell_format)
				worksheet.write(counter, 13,str(item2.Fecha_tdc),cell_format)
				worksheet.write(counter, 14,item2.TDC,cell_format)
				worksheet.write(counter, 15,item2.BS,cell_format)
				worksheet.write(counter, 16,item2.USD,cell_format)


		consulta3 = claculo_testigo.objects.filter(Barra=item.id)
		if(consulta3):
			for item3 in consulta3:
				cell_format = workbook.add_format({'bold': True , 'font_color': 'green'})

				worksheet.write(counter, 17,item3.Peso_final,cell_format)#kg
				worksheet.write(counter, 18,str(item3.Fecha_fixing),cell_format)
				worksheet.write(counter, 19,item3.Fixing,cell_format)
				worksheet.write(counter, 20,str(item3.Fecha_tdc),cell_format)
				worksheet.write(counter, 21,item3.TDC,cell_format)
				worksheet.write(counter, 22,item3.BS,cell_format)
				worksheet.write(counter, 23,item3.USD,cell_format)


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


def consultar3(request):
	if request.user.is_authenticated:
		context = {}

		if request.method == 'POST':
			form = ReportCodBarraForm(request.POST)
			if form.is_valid():
				return CreateExcel2(request,form.cleaned_data.get("Cod_barra"))
		else:
			form = ReportCodBarraForm()

		context['form']=form
		return render(request,'consultar_cod_barra.html',context)

	else:
		return HttpResponse("index")

		




def CreateExcel4(request,Estatus):
	output = io.BytesIO()

	workbook = xlsxwriter.Workbook(output)
	worksheet = workbook.add_worksheet()


	counter = 0	
	titulos = ['Num operacion','Derechante','Estatus','Complejo','Empresa','Cod barra','Peso bruto','Num guia','Num caja','Fecha Certificado','Peso Final','Fecha Fixing','Fixing','Fecha TDC','TDC','BS','USD','Peso Final','Fecha Fixing','Fixing','Fecha TDC','TDC','BS','USD']
	
	for key,value in enumerate(titulos):
		if key < 8 :
			cell_format = workbook.add_format({'bold': True , 'font_color': 'red'})
		if key > 8 and key <16:
			cell_format = workbook.add_format({'bold': True , 'font_color': 'blue'})
		if key > 16 and key <23:
			cell_format = workbook.add_format({'bold': True , 'font_color': 'green'})

		worksheet.write(0, key, value,cell_format)

	consulta = Barra.objects.filter(Estatus=Estatus)
	for item in consulta:
		counter +=1
		cell_format = workbook.add_format({'bold': True , 'font_color': 'red'})
		worksheet.write(counter, 0, item.num_operacion,cell_format)
		worksheet.write(counter, 1, str(item.Derechante),cell_format)
		worksheet.write(counter, 2, str(item.Estatus),cell_format)
		worksheet.write(counter, 3, str(item.Complejo),cell_format)
		worksheet.write(counter, 4, str(item.Empresa),cell_format)
		worksheet.write(counter, 5, item.Cod_barra,cell_format)
		worksheet.write(counter, 6, item.peso_bruto,cell_format)
		worksheet.write(counter, 7, str(item.Num_guia_onafin),cell_format)
		worksheet.write(counter, 8, item.num_caja,cell_format)


		consulta2 = calculo_barra.objects.filter(Barra=item.id)

		if(consulta2):
			for item2 in consulta2:
				cell_format = workbook.add_format({'bold': True , 'font_color': 'blue'})
				worksheet.write(counter, 9,str(item2.Fecha_certificado),cell_format)
				worksheet.write(counter, 10,item2.Ley,cell_format)
				worksheet.write(counter, 11,item2.Peso_final,cell_format)#kg
				worksheet.write(counter, 11,str(item2.Fecha_fixing),cell_format)
				worksheet.write(counter, 12,item2.Fixing,cell_format)
				worksheet.write(counter, 13,str(item2.Fecha_tdc),cell_format)
				worksheet.write(counter, 14,item2.TDC,cell_format)
				worksheet.write(counter, 15,item2.BS,cell_format)
				worksheet.write(counter, 16,item2.USD,cell_format)


		consulta3 = claculo_testigo.objects.filter(Barra=item.id)
		if(consulta3):
			for item3 in consulta3:
				cell_format = workbook.add_format({'bold': True , 'font_color': 'green'})

				worksheet.write(counter, 17,item3.Peso_final,cell_format)#kg
				worksheet.write(counter, 18,str(item3.Fecha_fixing),cell_format)
				worksheet.write(counter, 19,item3.Fixing,cell_format)
				worksheet.write(counter, 20,str(item3.Fecha_tdc),cell_format)
				worksheet.write(counter, 21,item3.TDC,cell_format)
				worksheet.write(counter, 22,item3.BS,cell_format)
				worksheet.write(counter, 23,item3.USD,cell_format)


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

def consultar4(request):
	if request.user.is_authenticated:
		context = {}

		if request.method == 'POST':
			form = ReportEstatusForm(request.POST)
			if form.is_valid():
				return CreateExcel4(request,form.cleaned_data.get("Estatus"))
				'''consulta = Barra.objects.filter(Estatus=form.cleaned_data.get("Estatus"))
				
				for item in consulta:
					print("barra")
					print(item.num_operacion)
					print(item.Derechante)
					print(item.Estatus)
					print(item.Complejo)
					print(item.Empresa)
					print(item.Cod_barra)
					print(item.peso_bruto)
					print(item.Num_guia_onafin)
					print(item.num_caja)
					print("->",item.id)'''
		else:
			form = ReportEstatusForm()

		context['form']=form
		return render(request,'consultar_estatus.html',context)

	else:
		return HttpResponse("index")




def CreateExcel5(request,num_operacion):
	output = io.BytesIO()

	workbook = xlsxwriter.Workbook(output)
	worksheet = workbook.add_worksheet()


	counter = 0	
	titulos = ['Num operacion','Derechante','Estatus','Complejo','Empresa','Cod barra','Peso bruto','Num guia','Num caja','Fecha Certificado','Peso Final','Fecha Fixing','Fixing','Fecha TDC','TDC','BS','USD','Peso Final','Fecha Fixing','Fixing','Fecha TDC','TDC','BS','USD']
	
	for key,value in enumerate(titulos):
		if key < 8 :
			cell_format = workbook.add_format({'bold': True , 'font_color': 'red'})
		if key > 8 and key <16:
			cell_format = workbook.add_format({'bold': True , 'font_color': 'blue'})
		if key > 16 and key <23:
			cell_format = workbook.add_format({'bold': True , 'font_color': 'green'})

		worksheet.write(0, key, value,cell_format)

	consulta = Barra.objects.filter(num_operacion=num_operacion)
	for item in consulta:
		counter +=1
		cell_format = workbook.add_format({'bold': True , 'font_color': 'red'})
		worksheet.write(counter, 0, item.num_operacion,cell_format)
		worksheet.write(counter, 1, str(item.Derechante),cell_format)
		worksheet.write(counter, 2, str(item.Estatus),cell_format)
		worksheet.write(counter, 3, str(item.Complejo),cell_format)
		worksheet.write(counter, 4, str(item.Empresa),cell_format)
		worksheet.write(counter, 5, item.Cod_barra,cell_format)
		worksheet.write(counter, 6, item.peso_bruto,cell_format)
		worksheet.write(counter, 7, str(item.Num_guia_onafin),cell_format)
		worksheet.write(counter, 8, item.num_caja,cell_format)


		consulta2 = calculo_barra.objects.filter(Barra=item.id)

		if(consulta2):
			for item2 in consulta2:
				cell_format = workbook.add_format({'bold': True , 'font_color': 'blue'})
				worksheet.write(counter, 9,str(item2.Fecha_certificado),cell_format)
				worksheet.write(counter, 10,item2.Ley,cell_format)
				worksheet.write(counter, 11,item2.Peso_final,cell_format)#kg
				worksheet.write(counter, 11,str(item2.Fecha_fixing),cell_format)
				worksheet.write(counter, 12,item2.Fixing,cell_format)
				worksheet.write(counter, 13,str(item2.Fecha_tdc),cell_format)
				worksheet.write(counter, 14,item2.TDC,cell_format)
				worksheet.write(counter, 15,item2.BS,cell_format)
				worksheet.write(counter, 16,item2.USD,cell_format)


		consulta3 = claculo_testigo.objects.filter(Barra=item.id)
		if(consulta3):
			for item3 in consulta3:
				cell_format = workbook.add_format({'bold': True , 'font_color': 'green'})

				worksheet.write(counter, 17,item3.Peso_final,cell_format)#kg
				worksheet.write(counter, 18,str(item3.Fecha_fixing),cell_format)
				worksheet.write(counter, 19,item3.Fixing,cell_format)
				worksheet.write(counter, 20,str(item3.Fecha_tdc),cell_format)
				worksheet.write(counter, 21,item3.TDC,cell_format)
				worksheet.write(counter, 22,item3.BS,cell_format)
				worksheet.write(counter, 23,item3.USD,cell_format)


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

def consultar5(request):
	if request.user.is_authenticated:
		context = {}

		if request.method == 'POST':
			form = ReportNum_OperacionForm(request.POST)
			if form.is_valid():
				return CreateExcel5(request,form.cleaned_data.get("num_operacion"))
				'''consulta = Barra.objects.filter(Estatus=form.cleaned_data.get("Estatus"))
				
				for item in consulta:
					print("barra")
					print(item.num_operacion)
					print(item.Derechante)
					print(item.Estatus)
					print(item.Complejo)
					print(item.Empresa)
					print(item.Cod_barra)
					print(item.peso_bruto)
					print(item.Num_guia_onafin)
					print(item.num_caja)
					print("->",item.id)'''
		else:
			form = ReportNum_OperacionForm()

		context['form']=form
		return render(request,'consultar_num_operacion.html',context)

	else:
		return HttpResponse("index")





def CreateExcel6(request,num_caja):
	output = io.BytesIO()

	workbook = xlsxwriter.Workbook(output)
	worksheet = workbook.add_worksheet()


	counter = 0	
	titulos = ['Num operacion','Derechante','Estatus','Complejo','Empresa','Cod barra','Peso bruto','Num guia','Num caja','Fecha Certificado','Peso Final','Fecha Fixing','Fixing','Fecha TDC','TDC','BS','USD','Peso Final','Fecha Fixing','Fixing','Fecha TDC','TDC','BS','USD']
	
	for key,value in enumerate(titulos):
		if key < 8 :
			cell_format = workbook.add_format({'bold': True , 'font_color': 'red'})
		if key > 8 and key <16:
			cell_format = workbook.add_format({'bold': True , 'font_color': 'blue'})
		if key > 16 and key <23:
			cell_format = workbook.add_format({'bold': True , 'font_color': 'green'})

		worksheet.write(0, key, value,cell_format)

	consulta = Barra.objects.filter(num_caja=num_caja)
	for item in consulta:
		counter +=1
		cell_format = workbook.add_format({'bold': True , 'font_color': 'red'})
		worksheet.write(counter, 0, item.num_operacion,cell_format)
		worksheet.write(counter, 1, str(item.Derechante),cell_format)
		worksheet.write(counter, 2, str(item.Estatus),cell_format)
		worksheet.write(counter, 3, str(item.Complejo),cell_format)
		worksheet.write(counter, 4, str(item.Empresa),cell_format)
		worksheet.write(counter, 5, item.Cod_barra,cell_format)
		worksheet.write(counter, 6, item.peso_bruto,cell_format)
		worksheet.write(counter, 7, str(item.Num_guia_onafin),cell_format)
		worksheet.write(counter, 8, item.num_caja,cell_format)


		consulta2 = calculo_barra.objects.filter(Barra=item.id)

		if(consulta2):
			for item2 in consulta2:
				cell_format = workbook.add_format({'bold': True , 'font_color': 'blue'})
				worksheet.write(counter, 9,str(item2.Fecha_certificado),cell_format)
				worksheet.write(counter, 10,item2.Ley,cell_format)
				worksheet.write(counter, 11,item2.Peso_final,cell_format)#kg
				worksheet.write(counter, 11,str(item2.Fecha_fixing),cell_format)
				worksheet.write(counter, 12,item2.Fixing,cell_format)
				worksheet.write(counter, 13,str(item2.Fecha_tdc),cell_format)
				worksheet.write(counter, 14,item2.TDC,cell_format)
				worksheet.write(counter, 15,item2.BS,cell_format)
				worksheet.write(counter, 16,item2.USD,cell_format)


		consulta3 = claculo_testigo.objects.filter(Barra=item.id)
		if(consulta3):
			for item3 in consulta3:
				cell_format = workbook.add_format({'bold': True , 'font_color': 'green'})

				worksheet.write(counter, 17,item3.Peso_final,cell_format)#kg
				worksheet.write(counter, 18,str(item3.Fecha_fixing),cell_format)
				worksheet.write(counter, 19,item3.Fixing,cell_format)
				worksheet.write(counter, 20,str(item3.Fecha_tdc),cell_format)
				worksheet.write(counter, 21,item3.TDC,cell_format)
				worksheet.write(counter, 22,item3.BS,cell_format)
				worksheet.write(counter, 23,item3.USD,cell_format)


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

def consultar6(request):
	if request.user.is_authenticated:
		context = {}

		if request.method == 'POST':
			form = ReportNum_CajaForm(request.POST)
			if form.is_valid():
				return CreateExcel6(request,form.cleaned_data.get("num_caja"))
				'''consulta = Barra.objects.filter(Estatus=form.cleaned_data.get("Estatus"))
				
				for item in consulta:
					print("barra")
					print(item.num_operacion)
					print(item.Derechante)
					print(item.Estatus)
					print(item.Complejo)
					print(item.Empresa)
					print(item.Cod_barra)
					print(item.peso_bruto)
					print(item.Num_guia_onafin)
					print(item.num_caja)
					print("->",item.id)'''
		else:
			form = ReportNum_CajaForm()

		context['form']=form
		return render(request,'consulta_ubicacion.html',context)

	else:
		return HttpResponse("index")


def consultar(request):
	if request.user.is_authenticated:
		context = {}

		if request.method == 'POST':
			form = ReportForm(request.POST)
			if form.is_valid():
				'''print(form.cleaned_data.get("fecha_inicio"),form.cleaned_data.get("fecha_fin"))
				
				consulta = Barra.objects.filter(created__range=[form.cleaned_data.get("fecha_inicio"),form.cleaned_data.get("fecha_fin")])
				
				for item in consulta:
					print("barra")
					print(item.num_operacion)
					print(item.Derechante)
					print(item.Estatus)
					print(item.Complejo)
					print(item.Empresa)
					print(item.Cod_barra)
					print(item.peso_bruto)
					print(item.Num_guia_onafin)
					print(item.num_caja)
					print("->",item.id)

					
					consulta2 = calculo_barra.objects.filter(Barra=item.id)
					if(consulta2):
						print("calculo barra")
						for item2 in consulta2:
							print(item2.Fecha_certificado)
							print(item2.Ley)
							print(item2.Peso_final)#kg
							print(item2.Fecha_fixing)
							print(item2.Fixing)
							print(item2.Fecha_tdc)
							print(item2.TDC)
							print(item2.BS)
							print(item2.USD)
							print("->",item.id)

					consulta3 = claculo_testigo.objects.filter(Barra=item.id)
					if(consulta3):
						print("calculo testigo")
						for item3 in consulta3:
							print(item3.Fecha_certificado)
							print(item3.Ley)
							print(item3.Peso_final)#kg
							print(item3.Fecha_fixing)
							print(item3.Fixing)
							print(item3.Fecha_tdc)
							print(item3.TDC)
							print(item3.BS)
							print(item3.USD)
							print("->",item3.id)'''


				return CreateExcel(request,form.cleaned_data.get("fecha_inicio"),form.cleaned_data.get("fecha_fin"))
				#return redirect('consultar')
		else:
			form = ReportForm()

		context['form']=form
		return render(request,'consultar.html',context)

	else:
		return HttpResponse("index")




def pesoFino(peso,ley):
	return peso * (ley / 1000)

def onzaTroy(peso,onza):
	return peso * onza

def valorUsd(fixing,onza):
	return fixing * onza

def valorBs(usd,tasa):
	return usd * tasa



def calcular_barra(request):
	if request.user.is_authenticated:
		context = {}
		if request.method == 'POST':
			form = CalculoBarraForm(request.POST)
			if form.is_valid():
				data = form.save(commit=False)
				data.creator = request.user
				peso=float(data.Peso_final)
				ley=float(data.Ley)
				fixing=float(data.Fixing)
				tasa=float(data.TDC)
				peso_fino = pesoFino(peso,ley)# peso*(ley/1000)
				onza_troy = onzaTroy(peso_fino,32.150743)# peso_fino*32.150743
				barra_usd = valorUsd(fixing,onza_troy)# fixing*onza_troy
				barra_bs = valorBs(barra_usd,tasa)# barra_usd*tasa
				data.BS=barra_bs
				data.USD=barra_usd
 
				print("*****************************************************")
				print("peso fino: ",peso_fino) 
				print("onza troy: ",onza_troy)
				print("usd: ",barra_usd)  
				print("bs: ",barra_bs)
				print("*****************************************************")
				data.save()
				return redirect('calculo_barra')
		else:
			form = CalculoBarraForm()
		context['form']=form
		return render(request,'calcular-barra.html',context)

	else:
		return HttpResponse("calculo_barra")

def list_view(request):
	if request.user.is_authenticated:
		context = {}
		context['form']=Barra.objects.all()
		urls = ['eliminar','modificar','detalles']
		context['urls']=urls
		return render(request,'list.html',context)
		 
	else:
		return HttpResponse("index")


class ProductoDeleteView(LoginRequiredMixin,DeleteView):
	model = Barra
	template_name = 'eliminar.html'
	permission_denied_message = 'No tienes permisos'
	success_url = reverse_lazy("list")


class ProductoUpdateView(LoginRequiredMixin,UpdateView):
	model = Barra
	form_class = ModificarForm
	template_name = 'modificar.html'
	permission_denied_message = 'No tienes permisos'
	success_url = reverse_lazy('list')



def detalles(request,pk):
	if request.user.is_authenticated:
		context = {}


		consulta = Barra.objects.filter(id=pk)
		consulta2 = calculo_barra.objects.filter(Barra=pk)
		consulta3 = claculo_testigo.objects.filter(Barra=pk)
		context['form']=consulta
		context['calculo1']=consulta2
		context['calculo2']=consulta3
		 
		print(consulta2,consulta3)



		return render(request,'detalles.html',context)

	else:
		return HttpResponse("index")



'''
def modificar(request,id):
	if request.user.is_authenticated:
		context = {}

		if request.method == 'POST':
			barra = Barra.objects.get(id=id)
			form = ModificarForm(request.POST)
			if form.is_valid():
				data = form.save(commit=False)
				data.creator = request.user

				
				#data.save()
				return redirect('modificar')
		else:
			form = ModificarForm()
		context['form']=form
		return render(request,'modificar',context)

	else:
		return HttpResponse("index")
'''

def calcular_testigo(request):
	if request.user.is_authenticated:
		context = {}

		if request.method == 'POST':
			
			form = CalculoTestigoForm(request.POST)
			if form.is_valid():
				data = form.save(commit=False)
				data.creator = request.user

				peso=float(data.Peso_final)
				ley=float(data.Ley)
				fixing=float(data.Fixing)
				tasa=float(data.TDC)
				peso_fino = pesoFino(peso,ley)# peso*(ley/1000)
				onza_troy = onzaTroy(peso_fino,0.032150743)# peso_fino*32.150743
				barra_usd = valorUsd(fixing,onza_troy)# fixing*onza_troy
				barra_bs = valorBs(barra_usd,tasa)# barra_usd*tasa
				data.BS=barra_bs
				data.USD=barra_usd
 
				print("*****************************************************")
				print("peso fino: ",peso_fino) 
				print("onza troy: ",onza_troy)
				print("usd: ",barra_usd)  
				print("bs: ",barra_bs)
				print("*****************************************************")
				data.save()
				return redirect('calcular_testigo')
		else:
			form = CalculoTestigoForm()
		context['form']=form
		return render(request,'calcular-testigo.html',context)

	else:
		return HttpResponse("index")