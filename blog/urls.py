from django.urls import path
from .import views


urlpatterns = [
    path('page/<int:pagina>/', views.blog,name='Blog'),
    path('buscar_blog/', views.buscar_blog, name="Buscar_blog"),
    path('categoria/<int:categoria_id>/', views.categoria, name="categoria"),
]