from django.shortcuts import render
from blog.models import Categoria, Post
from bootcamps.models import Tipo_Categoria
from django.core.paginator import Paginator, EmptyPage, InvalidPage #paginacion de Django


# Create your views here.


def blog(request, pagina):
    categBd= Categoria.objects.all()#Categorías de blog
    blogs= Post.objects.all().order_by('-id')[:5]#Publicaciones o blog Max 5
    tipo_categBd= Tipo_Categoria.objects.all() #categorías de Bootcamp

    # Método de paginación para los blogs			
    blogBd = Post.objects.all().order_by('-id')#Blogs
    paginator = Paginator(blogBd,4)
    try:
        page = int(pagina)
    except:
        page = 1
    try:
        blogs = paginator.page(page)
    except:
        blogs = paginator.page(paginator.num_pages)

    index = blogs.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 3 if index >= 3 else 0
    end_index = index + 3 if index <= max_index -3 else max_index
    page_range = paginator.page_range[start_index:end_index]

    return render(request, "blog/blog.html",{"categBd":categBd,"blogs":blogs,
                            "tipo_categBd":tipo_categBd,"blogs":blogs,"page_range":page_range})

def categoria(request, categoria_id):
    categBd= Categoria.objects.all()#Categorías de blog
    tipo_categBd= Tipo_Categoria.objects.all()#categorías de Bootcamp
    categoria=Categoria.objects.get(id=categoria_id)
    blogs= Post.objects.filter(categorias=categoria)

    return render(request,"blog/categoria.html", {"categoria":categoria,"tipo_categBd":tipo_categBd, "blogs":blogs, "categBd":categBd})

def buscar_blog(request):
    categBd = Categoria.objects.all()#Categorías de blog
    blogs = Post.objects.all().order_by('-id')#Publicaciones o blog Max 5
    tipo_categBd= Tipo_Categoria.objects.all()#categorías de Bootcamp

    if request.GET["blog"]:

        blog_select=request.GET["blog"]

        if len(blog_select)>20:
            mensaje_error="Texto de búsquedad demasiado largo!!"
        else:
            blogs=Post.objects.filter(titulo__icontains=blog_select)
            return render(request, "blog/blog.html",{"tipo_categBd":tipo_categBd,
            "categBd":categBd,"blogs":blogs})

    else:
        mensaje_error="Introduzca una busquedad!!"

    return render(request, "blog/blog.html",{"tipo_categBd":tipo_categBd,
    "categBd":categBd,"mensaje_error":mensaje_error,"blogs":blogs})