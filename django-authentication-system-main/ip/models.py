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

class cargos(BaseModelSimple):
	tipo = models.CharField(max_length=100)
	def __str__(self):
		return f"{self.tipo}"

class registro_ip(BaseModelSimple):
	#usuario = models.ForeignKey(User,on_delete=models.CASCADE,related_name='usuario')
	usuario = models.CharField(max_length=50)
	direccion = models.ForeignKey(direcciones,on_delete=models.DO_NOTHING,blank=True)
	cargo = models.ForeignKey(cargos,on_delete=models.DO_NOTHING,blank=True)
	ip = models.CharField(max_length=50,unique=True)
	mac = models.CharField(max_length=50,blank=True,null=True)
	tlf = models.CharField(max_length=50,blank=True,null=True)
	mactlf = models.CharField(max_length=50,blank=True,null=True)

	def __str__(self):
		return f" {self.usuario} - {self.direccion} - {self.cargo} - {self.ip} - {self.mac} - {self.tlf} - {self.mactlf}"
