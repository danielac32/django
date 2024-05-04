import os
from django.db import models
from django.db.models import CharField
from django.contrib.auth.models import User
from uuid import uuid4

from datetime import date
from datetime import datetime
# Create your models here.


class BaseModelSimple(models.Model):
	created = models.DateTimeField(auto_now=True)
	modified = models.DateTimeField(auto_now=True)

	class Meta:
		abstract=True

class BaseModel(BaseModelSimple):
	""" modelo base que heredan los demas modelos para llevar el control de objetos """
	creator = models.ForeignKey(User,on_delete=models.CASCADE)
	'''status = models.BooleanField(default=True)
	editable = models.BooleanField(default=True)
	visible = models.BooleanField(default=True)'''

	class Meta:
		abstract=True


class Categoria(BaseModel):
	tipo = models.CharField(max_length=50)

	def __str__(self):
		return f"{self.tipo}"


class oficina(models.Model):
	oficina = models.CharField(max_length=50)

	def __str__(self):
		return f"{self.oficina}"

def get_path(instance,filename):
	ext = filename.split(".")[-1]
	filename_uuid = f"{uuid4()}.{ext}"	
	x = str(instance.oficina).replace(" ", "_")
	return f"static/URL_DIRECCIONES/{x}/{filename_uuid}"

class Recepcion(BaseModel):
	persona = models.CharField(max_length=255,null=True)
	telefono = models.CharField(max_length=255,null=True)
	mensajero = models.CharField(max_length=255,verbose_name="mensajero")
	asunto = models.CharField(max_length=50)
	correlativo = models.AutoField(primary_key=True)
	fecha = models.DateField(auto_now=True)
	rif_ci = models.CharField(max_length=50)
	oficina = models.ForeignKey(oficina,on_delete=models.CASCADE)
	estatus = models.BooleanField(default=False,null=True)
	imagen = models.FileField(null=True,upload_to=get_path)

	def __str__(self):
		return f" {self.mensajero} - {self.asunto} - {self.oficina}"

'''class Archivos(BaseModelSimple):
	recepcion = models.ForeignKey(Recepcion,on_delete=models.CASCADE)
	imagen = models.FileField(null=True,upload_to=get_path)

	def __str__(self):
		return f"{self.imagen}"'''

class Oficio(BaseModel):
	usuario = models.ForeignKey(User,on_delete=models.CASCADE,related_name='usuario')
	recepcion = models.ForeignKey(Recepcion,on_delete=models.CASCADE)
	categoria   = models.ForeignKey(Categoria,on_delete=models.CASCADE)
	enviado = models.BooleanField(default=True)
	entregado = models.BooleanField(default=False)
	visto = models.BooleanField(default=False)
	devolver = models.BooleanField(default=False)
	urgente = models.BooleanField(default=False)
	estatus = models.BooleanField(default=False)
	observacion = models.TextField()
	ejecutado = models.BooleanField(default=False,null=True)


	def get_enviado(self):
		return  f"{self.enviado}"

	def get_absolute_url(self):
		return f"{self.pk}"
		
	def get_url_delete(self):
		return f"/borrar-oficio/{self.pk}/"

	def get_url_editar(self):
		return f"/editar-oficio/{self.pk}/"

	def get_url_detalle(self):
		return f"/detalle-oficio/{self.pk}/"

	def get_image_url(self):
		return f"/detalle-oficio/{self.pk}/"


	def __str__(self):
		if self.devolver == True:
			s_devolver="devuelto"
		else:
			s_devolver=""
		if self.enviado == True:
			s_enviado="enviado"
		if self.visto == True:
			s_visto= "visto"
		else:
			s_visto=""
		if self.entregado == True:
			s_entregado = "entregado"
		else:
			s_entregado=""
		if self.urgente == True:
			s_urgente="urgente"
		else:
			s_urgente=""

		return f"{self.usuario} - {self.recepcion} - {self.categoria} - {s_enviado} - {s_entregado} - {s_visto} - {s_urgente} - {s_devolver}"
