from django.forms import ModelForm
from .models import *
from django import forms
from django.db.models import Prefetch
from django.contrib.auth.models import Group
from .fields import GroupedModelChoiceField
from datetime import datetime
from django.core.exceptions import ValidationError
'''class CategoriaForm(ModelForm):
    class Meta:
      model = Categoria
      fields = ['tipo',]'''

 

class RecepcionForm(forms.ModelForm):
    class Meta:
        model = Recepcion

        fields =  (
                  'persona',
                  'telefono',
                  'mensajero',
                  'asunto',
                  'rif_ci',
                  'oficina',
                  'imagen')

        def __init__(self, *args, **kwargs):
            super(RecepcionForm, self).__init__(*args, **kwargs)
            self.fields['persona'].widget.attrs['placeholder'] = self.label
'''
class RecepcionForm(forms.ModelForm):
    imagen = forms.FileField(widget=forms.FileInput(attrs={'multiple': True}), required=True)

    class Meta:
        model = Recepcion
        fields =  ('mensajero',
                  'asunto',
                  'rif_ci',
                  'oficina',
                  'imagen')

    def save(self, *args, **kwargs):
        # multiple file upload
        # NB: does not respect 'commit' kwarg
        file_list = natsorted(self.files.getlist('{}-image'.format(self.prefix)), key=lambda file: file.name)
        recepcion_base = Recepcion.objects.create(
            mensajero = self.cleaned_data['mensajero'],
            asunto = self.cleaned_data['asunto'],
            )

        self.instance.image = file_list[0]

        for file in file_list[1:]:
            
            Archivos.objects.create(
                recepcion = recepcion_base
                image=file,
            )

        return super().save(*args, **kwargs)
'''


class OficioForm2(forms.ModelForm):
    usuario=forms.ModelChoiceField(queryset = User.objects.exclude(groups=None),widget=forms.Select(attrs={'class': 'select2'}))
    recepcion=forms.ModelChoiceField(queryset = Recepcion.objects.filter(estatus=False),widget=forms.Select(attrs={'class': 'select2'}))
    class Meta:
        model = Oficio
        fields = (
                'usuario',
                'recepcion',
                'categoria',
                'urgente',
                    )
        widgets = {
            'recepcion': forms.Select(attrs={'class': 'select2'}),
        }


    def __init__(self, *args, **kwargs):
        super(OficioForm2, self).__init__(*args, **kwargs)
        choices = [(item.pk,f"{item.first_name} {item.last_name} - {item.groups.all().first().name.upper()}") for item in User.objects.exclude(groups=None)]
        self.fields["usuario"].choices = choices

        

class OficioForm3(forms.ModelForm):
#    usuario = GroupedModelChoiceField(queryset = User.objects.exclude(groups=None),choices_groupby='groups')
    usuario=forms.ModelChoiceField(queryset = User.objects.exclude(groups=None),widget=forms.Select(attrs={'class': 'select2'}))
    recepcion=forms.ModelChoiceField(queryset = Recepcion.objects.filter(estatus=False),widget=forms.Select(attrs={'class': 'select2'}))
    class Meta:
        model = Oficio
        fields = (
                'usuario',
                'recepcion',
                'categoria',
                'urgente',
                    )



    def __init__(self, *args, **kwargs):
        super(OficioForm3, self).__init__(*args, **kwargs)
        choices = [(item.pk,f"{item.first_name} {item.last_name} - {item.groups.all().first().name.upper()}") for item in User.objects.exclude(groups=None)]
        self.fields["usuario"].choices = choices


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

class rp(forms.Form):
    correo = forms.CharField(required=True,label="correo")
    nueva_clave = forms.CharField(required=True,label="nueva clave")

   

class OficioForm(forms.ModelForm):

   # direccion = forms.ModelChoiceField( queryset=Recepcion.objects.all())

   # usuario = forms.ModelChoiceField(queryset = Recepcion.objects.all())

    #usuario = forms.ModelChoiceField( choices=MEDIA_CHOICES)

    usuario=forms.ModelChoiceField(queryset = Recepcion.objects.all(), empty_label = "Choose a link")

    class Meta:
        model = Oficio
        fields = (
                  'usuario',
                  'recepcion',
                  'categoria',
                  'enviado',
                  'entregado',
                  'visto',
                  'urgente',
                  'devolver',
                  'observacion',
                  )
        


    def __init__(self, *args, **kwargs):
        super(OficioForm, self).__init__(*args, **kwargs)
        choices = [(item.pk,f"{item.first_name} {item.last_name} - {item.groups.all().first().name.upper()}") for item in User.objects.exclude(groups=None)]
        self.fields["usuario"].choices = choices



        '''widget = {
                'urgente': forms.BooleanField(label="kkj"),
                'usuario': forms.SelectMultiple(attrs={'required': True})

        }'''

        '''exclude = ['enviado',
                    'entregado',
                    'visto',
                    'urgente',
                    'devolver',
                    ]
'''

'''
class Observacion(forms.Form):
    observacion= forms.CharField(widget=forms.Textfield(attrs={'placeholder':'observaciones','id':'some_id'}),required=True)
    '''

