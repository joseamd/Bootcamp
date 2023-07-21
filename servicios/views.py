from django.shortcuts import render
from servicios.models import Servicio
from bootcamps.models import Tipo_Categoria
from blog.models import Categoria
from blog.models import Post


# Create your views here.

def servicios(request):
    categBd= Categoria.objects.all()#Categorías de blog
    blogs = Post.objects.all().order_by('-id')[:5]#Publicaciones o blog Max 5
    serviciosBd=Servicio.objects.all().order_by('id')#Servicios
    tipo_categBd= Tipo_Categoria.objects.all()#categorías de Bootcamp

    return render(request, "servicios/servicios.html",{"serviciosBd":serviciosBd,"tipo_categBd":tipo_categBd,
                            "blogs":blogs,"categBd":categBd})


def buscar_servicio(request):
    categBd= Categoria.objects.all()#Categorías de blog
    blogs = Post.objects.all().order_by('-id')[:5]#Publicaciones o blog Max 5
    serviciosBd=Servicio.objects.all()#Servicios
    tipo_categBd= Tipo_Categoria.objects.all()#categorías de Bootcamp

    if request.GET["servicio"]:

        servicio_select=request.GET["servicio"]

        if len(servicio_select)>20:
            mensaje_error="Texto de búsquedad demasiado largo!!"
        else:
            serviciosBd=Servicio.objects.filter(titulo__icontains=servicio_select)
            return render(request, "servicios/servicios.html",{"serviciosBd":serviciosBd,
                    "tipo_categBd":tipo_categBd,"blogs":blogs,"categBd":categBd})

    else:
        mensaje_error="Introduzca una busquedad!!"

    return render(request, "servicios/servicios.html",{"serviciosBd":serviciosBd,
            "tipo_categBd":tipo_categBd,"blogs":blogs,"categBd":categBd,"mensaje_error":mensaje_error})