from django.urls import path
from servicios import views


urlpatterns = [
    path('', views.servicios, name="Servicios"),
    path('buscar_servicio/', views.buscar_servicio, name="Buscar_servicio"),
]