from django.forms import ModelForm
from .models import *
from django import forms
from django.db.models import Prefetch
from django.contrib.auth.models import Group
#from .fields import GroupedModelChoiceField
from datetime import datetime
from django.core.exceptions import ValidationError
from django.core.exceptions import NON_FIELD_ERRORS




class registrar_ip(forms.ModelForm):	
	usuario = forms.CharField(label='Usuario',required=True,error_messages = {'required': "campo requerido..."})
	direccion = forms.ModelChoiceField(label='Direccion',queryset = direcciones.objects.all(),required=True,error_messages = {'required': "campo requerido..."})
	cargo = forms.ModelChoiceField(label='Cargo',queryset = cargos.objects.all(),required=True,error_messages = {'required': "campo requerido..."})
	ip = forms.CharField(label='IP',required=True,error_messages = {'required': "campo requerido..." , 'unique': "la ip ya esta asignada"})
	mac = forms.CharField(label='MAC',required=False)
	tlf = forms.CharField(label='Telefono',required=False)
	mactlf = forms.CharField(label='MAC',required=False)

	class Meta:
		model = registro_ip
		fields = [  'usuario',
					'direccion',
					'cargo',
					'ip',
					'mac',
					'tlf',
					'mactlf']