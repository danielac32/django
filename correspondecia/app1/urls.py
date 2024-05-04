"""correspondecia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app1 import views
from app1 import urls
from app1.views import index
#from app1.views import GeeksFormView


urlpatterns = [
    #path('',index,name='index'),
    path('rp',views.reset_password.as_view(),name='rp'),
    path('reporte',views.ExcelReport.as_view(),name='reporte'),

    path('descargar/<int:pk>/',views.descargar,name='descargar'),
    path('devolver/<int:pk>/',views.devolver,name='devolver'),
    path('ejecutado/<int:pk>/',views.ejecutado,name='ejecutado'),
    path('',views.index.as_view(),name='index'),
    path('lista-recepcion/',views.RecepcionListView.as_view(),name='list-reception'),
    path('crear-recepcion/',views.RecepcionCreateView.as_view(),name='create-reception'),
    #path('borrar-recepcion/<int:pk>/',views.RecepcionBorrarView.as_view(),name='borrar-reception'),
    path('editar-recepcion/<int:pk>/',views.RecepcionEditarView.as_view(),name='editar-reception'),
    path('detalle-recepcion/<int:pk>/',views.RecepcionDetalleView.as_view(),name='detalle-reception'),

    path('lista-oficio/',views.OficioListView.as_view(),name='list-oficio'),
    path('crear-oficio/',views.OficioCreateView.as_view(),name='create-oficio'),
    path('crear-oficio2/',views.OficioCreate2View.as_view(),name='create-oficio2'),
   # path('borrar-oficio/<int:pk>/',views.OficioBorrarView.as_view(),name='borrar-oficio'),
    path('editar-oficio/<int:pk>/',views.OficioEditarView.as_view(),name='editar-oficio'),
    path('detalle-oficio/<int:pk>/',views.OficioDetalleView.as_view(),name='detalle-oficio'),
    path('observacion/<int:pk>/',views.OficioObservacionView.as_view(),name='observacion'),
    path('devuelto/',views.OficioDevueltoList.as_view(),name='devuelto'),
    path('eliminarOficio/<int:pk>/',views.eliminarOficio,name='eliminarOficio'),
    path('eliminarRecepcion/<int:pk>/',views.eliminarRecepcion,name='eliminarRecepcion'),
]


'''
path('lista-categoria/',views.CategoriaListView.as_view(),name='list-category'),
    path('crear-categoria/',views.CategoriaCreateView.as_view(),name='create-category'),
    path('borrar-categoria/<int:pk>/',views.CategoriaBorrarView.as_view(),name='borrar-category'),
    path('editar-categoria/<int:pk>/',views.CategoriaEditarView.as_view(),name='editar-category'),
    path('detalle-categoria/<int:pk>/',views.CategoriaDetalleView.as_view(),name='detalle-category'),
'''