from django.shortcuts import render, redirect, get_object_or_404
from bootcamps.models import Bootcamp, Tipo_Categoria
from blog.models import Post, Categoria
from .forms import *
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
import requests
import simplejson
import json
from django.http import FileResponse
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, InvalidPage #paginacion de Django
from datetime import datetime

def bootcamps(request, pagina):
    categBd= Categoria.objects.all()#Categorías de blog
    blogs = Post.objects.all().order_by('-id')[:5]#Publicaciones o blog Max 5    
    tipo_categBd= Tipo_Categoria.objects.all()#categorías de Bootcamp
    fecha_actual= datetime.now()

    # Método de paginación para los bootcamps				
    bootcampBd = Bootcamp.objects.all().order_by('-fecha_inicio')#Bootcamps
    paginator = Paginator(bootcampBd,4)
    try:
        page = int(pagina)
    except:
        page = 1
    try:
        cursos = paginator.page(page)
    except:
        cursos = paginator.page(paginator.num_pages)

    index = cursos.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 3 if index >= 3 else 0
    end_index = index + 3 if index <= max_index -3 else max_index
    page_range = paginator.page_range[start_index:end_index]
    
    return render(request, "bootcamps/lista_bootcamps.html",{"bootcampBd":bootcampBd,"page_range":page_range,
                            "tipo_categBd":tipo_categBd,"blogs":blogs,"categBd":categBd,"cursos":cursos,"fecha_actual":fecha_actual})

def inscripcion(request, bootcamp_id,id):
    usuario_id = get_object_or_404(User, pk=id)  
    if request.user.is_authenticated :

        try:
            BootcampInscripcion.objects.get(usuario=id,bootcamp=bootcamp_id)
        except BootcampInscripcion.DoesNotExist:
            usuario = usuario_id.pk             
            if usuario:
                data = requests.get('https://www.mockly.app/api/8e7520e7-7dd0-4bfd-a129-71e7fe743453/estudiantes/%s' % usuario, verify=False)
                data_json = data.json()
                cedula = (data_json["cedula"])
                nombre= (data_json["nombre"])
                apellido= (data_json["apellido"])                        
                email= (data_json["email"])
                direccion= (data_json["direccion"])
                telefono= (data_json["telefono"])              
                carrera = (data_json["carrera"])              
                bootcamp = bootcamp_id                                       
            
                i = BootcampInscripcion()

                i.cedula  = cedula
                i.nombre = nombre
                i.apellido = apellido
                i.usuario = usuario_id
                i.email = email
                i.direccion = direccion
                i.telefono = telefono
                i.save()     #guarda la inscripcion en la bd                 
                i.carrera.add(carrera)      #seteamos el manytomany de carrera
                i.bootcamp.add(bootcamp)    #seteamos el manytomany de bootcamp

                messages.success(request, "Te has registrado correctamente!!")
            else:
                messages.error(request, "No existe información!!")
        else: 
            messages.error(request, "Ya te encuentras registrado en este Bootcamp!!")   
    else:
        return redirect("Iniciar_Sesion")
        
    return redirect('/bootcamps/page/1/')

def buscar_bootcamp(request):
    categBd= Categoria.objects.all()#Categorías de blog
    blogs = Post.objects.all().order_by('-id')[:5]#Publicaciones o blog Max 5
    cursos = Bootcamp.objects.all()#Bootcamps
    tipo_categBd= Tipo_Categoria.objects.all()#categorías de Bootcamp

    if request.GET["boot"]:

        bootcamp_select=request.GET["boot"]
        
        if len(bootcamp_select)>20:
            mensaje_error="Texto de búsquedad demasiado largo!!"
        else:
            #Se filtra busquedad por titulo ó por Autor
            cursos = Bootcamp.objects.filter(
                Q(titulo__icontains = bootcamp_select) |
                Q(autor__username = bootcamp_select)
            )  
            return render(request, "bootcamps/lista_bootcamps.html",{"tipo_categBd":tipo_categBd,
                    "blogs":blogs,"categBd":categBd,"cursos":cursos})

    else:
        mensaje_error="Introduzca una busquedad!!"

    return render(request, "bootcamps/lista_bootcamps.html",{"cursos":cursos,
            "tipo_categBd":tipo_categBd,"blogs":blogs,"categBd":categBd,"mensaje_error":mensaje_error})

def add_bootcamp(request, id):

    usuario_id = get_object_or_404(User, pk=id)
    form = AddBootcampForm()

    if request.user.is_authenticated :                
        if request.method == "POST":
            form = AddBootcampForm(request.POST,request.FILES)            
            if form.is_valid():               

                titulo = form.cleaned_data['titulo']
                contenido = form.cleaned_data['contenido']  
                imagen = form.cleaned_data['imagen']                               
                requisito1 = form.cleaned_data['requisito1']
                requisito2 = form.cleaned_data['requisito2']
                requisito3 = form.cleaned_data['requisito3']
                requisito4 = form.cleaned_data['requisito4']
                requisito5 = form.cleaned_data['requisito5']
                autor = usuario_id
                categoria = form.cleaned_data['categoria'] 
                fecha_inicio = form.cleaned_data['fecha_inicio']

                a = Bootcamp()

                a.titulo  = titulo
                a.contenido = contenido 
                a.imagen = imagen
                a.requisito1 = requisito1
                a.requisito2 = requisito2
                a.requisito3 = requisito3
                a.requisito4 = requisito4
                a.requisito5 = requisito5
                a.autor = autor
                a.fecha_inicio = fecha_inicio
                a.save()     #guarda bootcamp en la bd             
                a.categoria.add(categoria) 

                messages.success(request, "Bootcamp guardado correctamente!!")
                return redirect(request.META.get('HTTP_REFERER'))
                                                            
            else:                                             
                messages.error(request, "Datos incorrectos")
                return redirect(request.META.get('HTTP_REFERER'))
       
        return render(request, "bootcamps/add_bootcamp.html",{"form":form,"usuario_id":usuario_id })
    else:
        return redirect("Iniciar_Sesion")

def edit_bootcamp(request,id_bootcamp):

    bootcampBd = get_object_or_404(Bootcamp, pk=id_bootcamp)
    fecha_inicio = bootcampBd.fecha_inicio

    data = {
        'form': EditBootcampForm(instance=bootcampBd),
        'bootcampBd':bootcampBd,
        'fecha_inicio':fecha_inicio
    }      
    if request.user.is_authenticated:
        if request.method == "POST":
            form = EditBootcampForm(data=request.POST,instance= bootcampBd,files=request.FILES)            
            if form.is_valid():               
                form.save()
                fecha_inicio = request.POST.get('id_fecha_inicio')
                Bootcamp.objects.filter(pk=int(id_bootcamp)).update(fecha_inicio=fecha_inicio)
                messages.success(request, "Bootcamp Actualizado correctamente!!")
                return redirect(request.META.get('HTTP_REFERER'))
                                                            
            else:                                             
                messages.error(request, "Datos incorrectos")
                return redirect(request.META.get('HTTP_REFERER'))
        
        return render(request, "bootcamps/edit_bootcamp.html",data)
    else:
        return redirect("Iniciar_Sesion")

def delete_bootcamp(request,id_bootcamp):
    bootcampBd = get_object_or_404(Bootcamp, pk=id_bootcamp)
    bootcampBd.delete()
    messages.success(request, "Bootcamp eliminado correctamente!!") 
    return redirect(request.META.get('HTTP_REFERER'))