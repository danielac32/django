from django.contrib import admin
from inventario.models import *
# register your models here.

admin.site.register(Producto)
admin.site.register(Categoria)
admin.site.register(Modificacion)
admin.site.register(Direccion)
