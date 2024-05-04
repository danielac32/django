from django.forms import ModelForm
from .models import *
from django import forms
from django.db.models import Prefetch
from django.contrib.auth.models import Group
#from .fields import GroupedModelChoiceField
from datetime import datetime
from django.core.exceptions import ValidationError
from django.core.exceptions import NON_FIELD_ERRORS



class Ingresar_Categoria(forms.ModelForm):
	tipo = forms.CharField(label='Categoria',required=True,error_messages = {'required': "campo requerido..."})
	tipo.widget.attrs.update({'class': 'form-control'})
	class Meta:
		model = Categoria
		fields = ['tipo']
					

class Ingresar_Producto(forms.ModelForm):
	codigo = forms.CharField(label='Codigo',required=True,error_messages = {'required': "campo requerido..."})
	nombre = forms.CharField(label='Nombre',required=True,error_messages = {'required': "campo requerido..."})
	categoria = forms.ModelChoiceField(label='Categoria',queryset = Categoria.objects.all(),required=True,error_messages = {'required': "campo requerido..."},widget=forms.Select(attrs={'class': 'select2'})) #forms.CharField(label='Complejo',required=True)
	stock = forms.DecimalField(label='Stock')
	observacion = forms.CharField(label='Observacion',required=False,widget=forms.Textarea)
	
	codigo.widget.attrs.update({'class': 'form-control'})
	nombre.widget.attrs.update({'class': 'form-control'})
	categoria.widget.attrs.update({'class': 'form-control select2'})
	stock.widget.attrs.update({'class': 'form-control'})
	observacion.widget.attrs.update({'class': 'form-control'})

	class Meta:
		model = Producto
		fields = [  'codigo',
					'nombre',
					'categoria',
					'stock',
					'observacion']


class Editar_Producto(forms.ModelForm):
	codigo = forms.CharField(label='Codigo',required=True,error_messages = {'required': "campo requerido..."})
	nombre = forms.CharField(label='Nombre',required=True,error_messages = {'required': "campo requerido..."})
	categoria = forms.ModelChoiceField(label='Categoria',queryset = Categoria.objects.all(),required=True,error_messages = {'required': "campo requerido..."},widget=forms.Select(attrs={'class': 'select2'})) #forms.CharField(label='Complejo',required=True)
	observacion = forms.CharField(label='Observacion',required=False,widget=forms.Textarea)
	
	codigo.widget.attrs.update({'class': 'form-control'})
	nombre.widget.attrs.update({'class': 'form-control'})
	categoria.widget.attrs.update({'class': 'form-control select2'})
	observacion.widget.attrs.update({'class': 'form-control'})

	class Meta:
		model = Producto
		fields = [  'codigo',
					'nombre',
					'categoria',
					'observacion']


class Actualizar_stock(forms.Form):
	stock = forms.IntegerField(label='Agregar al stock',required=True,error_messages = {'required': "campo requerido..."})

	def clean_stock(self):
		data = self.cleaned_data['stock']
		if data < 0:
			raise ValidationError("No puedes poner numeros negativos")
		return data

class Actualizar_stock2(forms.Form):
	stock = forms.IntegerField(label='Restar al stock',required=True,error_messages = {'required': "campo requerido..."})
	direccion = forms.ModelChoiceField(label='Direccion',queryset = Direccion.objects.all(),required=True,error_messages = {'required': "campo requerido..."},widget=forms.Select(attrs={'class': 'select2'}))
	#stock.widget.attrs.update({'class': 'form-control'})

	def clean_stock(self):
		data = self.cleaned_data['stock']
		if data < 0:
			raise ValidationError("No puedes poner numeros negativos")
		return data


class ReportForm(forms.Form):
    fecha_inicio = forms.DateField(required=True,label="Fecha inicial",widget=forms.DateInput(attrs={'type': 'date' , 'class': 'form-control my-3'}))
    fecha_fin = forms.DateField(required=True,label="Fecha final",widget=forms.DateInput(attrs={'type': 'date' , 'class': 'form-control my-3'}))

    def clean(self):
        cleaned_data = super().clean()
        inicial = cleaned_data.get("fecha_inicio")
        final = cleaned_data.get("fecha_fin")
        if inicial is None or final is None:
            raise ValidationError("Debe incorporar una fecha valida")
        if inicial > final:
            raise ValidationError("La fecha de inicio no puede ser mayor a la fecha final")

