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


class direcciones(BaseModelSimple):
	tipo = models.CharField(max_length=100)
	def __str__(self):
		return f"{self.tipo}"


class reporte_soporte(BaseModelSimple):
	usuario = models.CharField(max_length=50)
	direccion = models.ForeignKey(direcciones,on_delete=models.DO_NOTHING,blank=True)
	observacion = models.TextField()
	tlf = models.CharField(max_length=50,blank=True,null=True)
	estatus = models.BooleanField(blank=True,null=True)
	analista = models.CharField(max_length=50,blank=True,null=True)
	def __str__(self):
		return f" {self.usuario} - {self.direccion} - {self.observacion} - {self.tlf} - {self.estatus}"


