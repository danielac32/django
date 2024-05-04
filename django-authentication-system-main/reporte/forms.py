from django.forms import ModelForm
from .models import *
from django import forms
from django.db.models import Prefetch
from django.contrib.auth.models import Group
#from .fields import GroupedModelChoiceField
from datetime import datetime
from django.core.exceptions import ValidationError
from django.core.exceptions import NON_FIELD_ERRORS



class registrar(forms.ModelForm):	
	usuario = forms.CharField(label='Usuario',required=True,error_messages = {'required': "campo requerido..."})
	direccion = forms.ModelChoiceField(label='Direccion',queryset = direcciones.objects.all(),required=True,error_messages = {'required': "campo requerido..."})
	observacion = forms.CharField(label='Observacion',required=True,error_messages = {'required': "campo requerido..." , 'unique': "la ip ya esta asignada"},widget=forms.Textarea)
	tlf = forms.CharField(label='Telefono',required=False)
	#estatus = forms.CharField(label='Telefono',required=False)
	#analista = forms.CharField(label='Analista',required=True)

	class Meta:
		model = reporte_soporte
		fields = [  'usuario',
					'direccion',
					'observacion',
					'tlf']

					