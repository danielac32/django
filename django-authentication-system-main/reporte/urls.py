from django.contrib import admin
from django.urls import path
from reporte import views
from reporte import urls
#from reporte.views import index


urlpatterns = [
 path('index-reporte',views.index.as_view(),name='reporte'),
 path('registrar/',views.registrar_soporte.as_view(),name='registrar'),
 path('lista/',views.list.as_view(),name='lista'),
]
