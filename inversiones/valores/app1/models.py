import os
from django.db import models
from django.db.models import CharField
from django.contrib.auth.models import User
from uuid import uuid4

from datetime import date
from datetime import datetime

class BaseModelSimple(models.Model):
	created = models.DateTimeField(auto_now=True)
	modified = models.DateTimeField(auto_now=True)

	class Meta:
		abstract=True

class BaseModel(BaseModelSimple):
	""" modelo base que heredan los demas modelos para llevar el control de objetos """
	creator = models.ForeignKey(User,on_delete=models.CASCADE)
	class Meta:
		abstract=True


class Derechante(BaseModel):
	tipo= models.CharField(max_length=100)
	def __str__(self):
		return f"{self.tipo}"

class Estatus(BaseModel):
	tipo= models.CharField(max_length=100)
	def __str__(self):
		return f"{self.tipo}"

class Empresa(BaseModel):
	tipo= models.CharField(max_length=100)
	def __str__(self):
		return f"{self.tipo}"

class Complejo(BaseModel):
	tipo= models.CharField(max_length=100)
	def __str__(self):
		return f"{self.tipo}"


 

class Barra(BaseModel):
	num_operacion = models.IntegerField()
	Derechante = models.ForeignKey(Derechante,on_delete=models.CASCADE)
	Estatus = models.ForeignKey(Estatus,on_delete=models.CASCADE)
	Complejo = models.ForeignKey(Complejo,on_delete=models.CASCADE)
	Empresa = models.ForeignKey(Empresa,on_delete=models.CASCADE)
	Cod_barra = models.CharField(max_length=255,null=True)
	peso_bruto = models.DecimalField(max_digits = 10,decimal_places = 5)
	Num_guia_onafin = models.CharField(max_length=255,null=True)
	num_caja = models.IntegerField()
	def __str__(self):
		return f" {self.Cod_barra} "



class calculo_barra(BaseModel):
	Barra = models.OneToOneField(Barra,on_delete=models.CASCADE,null=True,error_messages ={"unique":"La Barra ya esta calculada!"})
	#Cod_barra = models.CharField(max_length=255,null=True)
	Fecha_certificado = models.DateField(auto_now=False)
	Ley = models.DecimalField(max_digits = 10,decimal_places = 5)
	Peso_final = models.DecimalField(max_digits = 10,decimal_places = 5)#kg
	Fecha_fixing = models.DateField()
	Fixing = models.DecimalField(max_digits = 10,decimal_places = 5)
	Fecha_tdc = models.DateField()
	TDC = models.DecimalField(max_digits = 10,decimal_places = 5)
	BS = models.DecimalField(max_digits = 10,decimal_places = 5,null=True)
	USD = models.DecimalField(max_digits = 10,decimal_places = 5,null=True)
	def __str__(self):
		return f" {self.Barra} - {self.BS} - {self.USD}"


class claculo_testigo(BaseModel):
	Barra = models.OneToOneField(Barra,on_delete=models.CASCADE,null=True,error_messages ={"unique":"El Testigo ya esta calculada!"})
	#Cod_barra = models.CharField(max_length=255,null=True)
	Fecha_certificado = models.DateField()
	Ley = models.DecimalField(max_digits = 10,decimal_places = 5)
	Peso_final = models.DecimalField(max_digits = 10,decimal_places = 5)#gr
	Fecha_fixing = models.DateField()
	Fixing = models.DecimalField(max_digits = 10,decimal_places = 5)
	Fecha_tdc = models.DateField()
	TDC = models.DecimalField(max_digits = 10,decimal_places = 5)
	BS = models.DecimalField(max_digits = 10,decimal_places = 5,null=True)
	USD = models.DecimalField(max_digits = 10,decimal_places = 5,null=True)
	def __str__(self):
		return f" {self.Barra} - {self.BS} - {self.USD}"




