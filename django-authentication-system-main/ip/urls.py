from django.contrib import admin
from django.urls import path
from ip import views
from ip import urls
#from ip.views import index


urlpatterns = [
path('index-ip',views.index.as_view(),name='ip'),
path('registrar-ip/',views.registrar.as_view(),name='registrar-ip'),
path('lista-ip/',views.ip_list.as_view(),name='lista-ip'),
path('eliminar-ip/<int:pk>/',views.ip_delete.as_view(),name='eliminar-ip'),
path('editar-ip/<int:pk>/',views.ip_update.as_view(),name='editar-ip'),
]
