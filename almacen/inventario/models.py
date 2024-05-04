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



class Categoria(models.Model):
	tipo = models.CharField(max_length=50)
	def __str__(self):
		return f"{self.tipo}"

class Direccion(models.Model):
	direccion = models.CharField(max_length=64)
	def __str__(self):
		return f"{self.direccion}"


class Modificacion(BaseModel):
	#producto = models.ForeignKey('Producto',on_delete=models.CASCADE,blank=True,null=True)
	tipo = models.CharField(max_length=50)
	direccion = models.CharField(max_length=50)
	id_producto = models.IntegerField()
	valor = models.IntegerField()

	def __str__(self):
		return f"{self.id_producto} - {self.tipo} - {self.valor} - {self.created}"

	
class Producto(BaseModel):
	#usuario = models.ForeignKey(User,on_delete=models.CASCADE,related_name='usuario')
	codigo = models.CharField(max_length=50)
	nombre = models.CharField(max_length=50)

	categoria = models.ForeignKey(Categoria,on_delete=models.CASCADE)
	stock = models.IntegerField(blank=True,null=True)
	observacion = models.TextField(blank=True,null=True)
	
	def __str__(self):
		return f" {self.id} - {self.codigo} - {self.nombre} - {self.categoria} - {self.stock} - {self.created}"

	def agregar_stock(self,numero):
		self.stock = self.stock + numero
		self.save()

	def restar_stock(self,numero):
		if numero < self.stock:
			self.stock = self.stock - numero
			self.save()




