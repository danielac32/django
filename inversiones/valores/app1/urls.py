from django.contrib import admin
from django.urls import path
from app1 import views
from app1 import urls
from app1.views import index,consultar2,consultar3,consultar4,consultar5,consultar6,ingresar_barra,calcular_barra,calcular_testigo,consultar,list_view,detalles#,modificar


urlpatterns = [
path('',index,name='index'),
path('consultar2',consultar2,name='consultar2'),
path('consultar3',consultar3,name='consultar3'),#consultar_cod_barra
path('consultar4',consultar4,name='consultar4'),#consultar_estatus
path('consultar5',consultar5,name='consultar5'),#num_operacion
path('consultar6',consultar6,name='consultar6'),#num_caja

path('ingresar',ingresar_barra,name='ingresar'),
path('calcular-barra',calcular_barra,name='calculo_barra'),
path('calcular-testigo',calcular_testigo,name='calcular_testigo'),
path('consultar',consultar,name='consultar'),
path('list',list_view,name='list'),

path('eliminar/<int:pk>/',views.ProductoDeleteView.as_view(),name='eliminar'),
path('modificar/<int:pk>/',views.ProductoUpdateView.as_view(),name='modificar'),

path('detalles/<int:pk>/',detalles,name='detalles'),

#path('',views.index.as_view(),name='index'),
#path('insertar',views.BarraCreate.as_view(),name='insert'),
#path('calcular-barra',views.CalculoBarraCreate.as_view(),name='calcular-barra'),
#path('calcular-testigo',views.CalculoTestigoCreate.as_view(),name='calcular-testigo'),
]