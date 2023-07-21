from django.shortcuts import render, HttpResponse
from bootcamps.models import Tipo_Categoria
from blog.models import Post, Categoria

# Create your views here.


def home(request):
    blogs = Post.objects.all().order_by('-id')[:5]#Publicaciones o blog Max 5
    tipo_categBd= Tipo_Categoria.objects.all()#categorías de Bootcamp
    categBd= Categoria.objects.all()#Categorías de blog

    return render(request, "home/home.html",{ "tipo_categBd":tipo_categBd , "blogs":blogs,
                        "categBd":categBd})









