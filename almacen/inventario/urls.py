from django.contrib import admin
from django.urls import path
from inventario import views
from inventario import urls
from inventario.views import index,SumarStockUpdateView,RestarStockUpdateView


urlpatterns = [
path('',index,name='index'),
path('crear-categoria/',views.CategoriaCreateView.as_view(),name='crear-categoria'),
path('crear-producto/',views.ProductoCreateView.as_view(),name='crear-producto'),
path('lista-producto/',views.ProductoListView.as_view(),name='lista-producto'),
path('eliminar-producto/<int:pk>/',views.ProductoDeleteView.as_view(),name='eliminar-producto'),
path('editar-producto/<int:pk>/',views.ProductoUpdateView.as_view(),name='editar-producto'),
path('sumar-stock/<int:pk>/',SumarStockUpdateView,name='sumar-stock'),
path('restar-stock/<int:pk>/',RestarStockUpdateView,name='restar-stock'),
path('reporte',views.ExcelReport.as_view(),name='reporte'),

]