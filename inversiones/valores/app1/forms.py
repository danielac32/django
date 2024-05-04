from django.forms import ModelForm
from .models import *
from django import forms
from django.db.models import Prefetch
from django.contrib.auth.models import Group
#from .fields import GroupedModelChoiceField
from datetime import datetime
from django.core.exceptions import ValidationError
from django.core.exceptions import NON_FIELD_ERRORS



class ReportForm(forms.Form):
    fecha_inicio = forms.DateField(required=True,label="Fecha inicial",widget=forms.DateInput(attrs={'type': 'date'}))
    fecha_fin = forms.DateField(required=True,label="Fecha final",widget=forms.DateInput(attrs={'type': 'date'}))

    def clean(self):
        cleaned_data = super().clean()
        inicial = cleaned_data.get("fecha_inicio")
        final = cleaned_data.get("fecha_fin")
        if inicial is None or final is None:
            raise ValidationError("Debe incorporar una fecha valida")
        if inicial > final:
            raise ValidationError("La fecha de inicio no puede ser mayor a la fecha final")

class ReportCodBarraForm(forms.Form):
	Cod_barra = forms.CharField(label='Codigo de Barra',required=True,error_messages = {'required': "campo requerido..."})
	
	def clean(self):
		cleaned_data = super().clean()
		inicial = cleaned_data.get("Cod_barra")


class ReportEstatusForm(forms.Form):
	Estatus = forms.ModelChoiceField(queryset = Estatus.objects.all())

	def clean(self):
		cleaned_data = super().clean()
		inicial = cleaned_data.get("Estatus")


class ReportCodBarraForm(forms.Form):
	Cod_barra = forms.CharField(label='Codigo de Barra',required=True,error_messages = {'required': "campo requerido..."})
	
	def clean(self):
		cleaned_data = super().clean()
		inicial = cleaned_data.get("Cod_barra")

class ReportNum_OperacionForm(forms.Form):
	num_operacion = forms.IntegerField(label='N° Operacion',required=True,error_messages = {'required': "campo requerido..."})

	def clean(self):
		cleaned_data = super().clean()
		inicial = cleaned_data.get("num_operacion")


class ReportNum_CajaForm(forms.Form):
	num_caja = forms.IntegerField(label='N° Caja',required=True,error_messages = {'required': "campo requerido..."})

	def clean(self):
		cleaned_data = super().clean()
		inicial = cleaned_data.get("num_caja")

class ModificarForm(forms.ModelForm):

	
	class Meta:
		model = Barra
		fields = [  'num_operacion',
					'Derechante',
					'Estatus',
					'Complejo',
					'Empresa',
					'Cod_barra',
					'peso_bruto',
					'Num_guia_onafin',
					'num_caja']



class BarraForm(forms.ModelForm):
	CHOICES =(
	    ("1", "ONT S/A"),
	    ("2", "ONT C/A"),
	    ("3", "BCV"),
	    ("4", "FONDEN/ENTREGADA"),
	)
	num_operacion = forms.IntegerField(label='N° Operacion',required=True,error_messages = {'required': "campo requerido..."})
	Derechante = forms.ModelChoiceField(queryset = Derechante.objects.all(),required=True,error_messages = {'required': "campo requerido..."}) #forms.CharField(label='Derechante',required=True)
	#Estatus = forms.ChoiceField(choices=CHOICES)#Estatus = forms.ModelChoiceField(queryset = Estatus.objects.filter(id=1)) #forms.CharField(label='Estatus',required=True)
	Estatus = forms.ModelChoiceField(queryset = Estatus.objects.all())

	Complejo = forms.ModelChoiceField(queryset = Complejo.objects.all(),required=True,error_messages = {'required': "campo requerido..."}) #forms.CharField(label='Complejo',required=True)
	Empresa = forms.ModelChoiceField(queryset = Empresa.objects.all(),required=True,error_messages = {'required': "campo requerido..."}) #forms.CharField(label='Empresa',required=True)

	Cod_barra = forms.CharField(label='Codigo de Barra',required=True,error_messages = {'required': "campo requerido..."})
	peso_bruto = forms.DecimalField(label='Peso Bruto',required=True,error_messages = {'required': "campo requerido..."})
	Num_guia_onafin = forms.CharField(label='N° Guia',required=True,error_messages = {'required': "campo requerido..."})
	num_caja = forms.IntegerField(label='N° Caja',required=True,error_messages = {'required': "campo requerido..."})

	class Meta:
		model = Barra
		fields = [  'num_operacion',
					'Derechante',
					'Estatus',
					'Complejo',
					'Empresa',
					'Cod_barra',
					'peso_bruto',
					'Num_guia_onafin',
					'num_caja']
					



class CalculoBarraForm(forms.ModelForm):
	Barra = forms.ModelChoiceField(queryset = Barra.objects.all(),required=True,widget=forms.Select(attrs={'class': 'select2'}))
	Fecha_certificado = forms.DateField(label='Fecha Certificado',required=True,error_messages = {'required': "campo requerido..."},widget=forms.DateInput(attrs={'type': 'date'}))
	Ley = forms.DecimalField(label='Ley',required=True,error_messages = {'required': "campo requerido..."})
	Peso_final = forms.DecimalField(label='Peso Final(kg)',required=True,error_messages = {'required': "campo requerido..."})#kg
	Fecha_fixing = forms.DateField(label='Fecha Fixing',required=True,error_messages = {'required': "campo requerido..."},widget=forms.DateInput(attrs={'type': 'date'}))
	Fixing = forms.DecimalField(label='Fixing',required=True,error_messages = {'required': "campo requerido..."})
	Fecha_tdc = forms.DateField(label='Fecha TDC',required=True,error_messages = {'required': "campo requerido..."},widget=forms.DateInput(attrs={'type': 'date'}))
	TDC = forms.DecimalField(label='TDC',required=True,error_messages = {'required': "campo requerido..."})

	class Meta:
		model = calculo_barra
		fields = [  'Barra',
					#'Cod_barra' ,
					'Fecha_certificado' ,
					'Ley' ,
					'Peso_final' ,
					'Fecha_fixing' ,
					'Fixing', 
					'Fecha_tdc' ,
					'TDC' ,
				]
		 
class CalculoTestigoForm(forms.ModelForm):
	Barra = forms.ModelChoiceField(queryset = Barra.objects.all(),required=True,error_messages = {'required': "campo requerido..."},widget=forms.Select(attrs={'class': 'select2'}))
	Fecha_certificado = forms.DateField(label='Fecha Certificado',required=True,error_messages = {'required': "campo requerido..."},widget=forms.DateInput(attrs={'type': 'date'}))
	Ley = forms.DecimalField(label='Ley',required=True,error_messages = {'required': "campo requerido..."})
	Peso_final = forms.DecimalField(label='Peso Final(kg)',required=True,error_messages = {'required': "campo requerido..."})#kg
	Fecha_fixing = forms.DateField(label='Fecha Fixing',required=True,error_messages = {'required': "campo requerido..."},widget=forms.DateInput(attrs={'type': 'date'}))
	Fixing = forms.DecimalField(label='Fixing',required=True,error_messages = {'required': "campo requerido..."})
	Fecha_tdc = forms.DateField(label='Fecha TDC',required=True,error_messages = {'required': "campo requerido..."},widget=forms.DateInput(attrs={'type': 'date'}))
	TDC = forms.DecimalField(label='TDC',required=True,error_messages = {'required': "campo requerido..."})

	class Meta:
		model = claculo_testigo
		fields = [  'Barra',
					#'Cod_barra' ,
					'Fecha_certificado' ,
					'Ley' ,
					'Peso_final' ,
					'Fecha_fixing' ,
					'Fixing', 
					'Fecha_tdc' ,
					'TDC' ,
				]
		 
					