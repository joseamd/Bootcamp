from django.shortcuts import render, redirect, get_object_or_404
from campus.models import *
from bootcamps.models import *
from django.contrib.auth.models import User
from django.contrib import messages
from campus.forms import *
from django.core.files.storage import FileSystemStorage
from django.db.models import Sum, Count,Avg
from django.db.models.functions import Round
from datetime import datetime, date
from django.db.models import Q

from django.http import JsonResponse
from django.shortcuts import render
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from django.http import HttpResponse


# Create your views here.

id_list = [] # variable global para obtener los id_asistencia

def campus(request):
    id_usuario = request.user.id
    usuario_id = get_object_or_404(User, pk=id_usuario)

    emisores = Notificaciones.objects.filter(usuario_receptor=usuario_id.pk).order_by('-created_at')[:5]
    totalNotificaciones= Notificaciones.objects.filter(usuario_receptor=usuario_id.pk).count()#cuenta la cantidad de Mensajes
    totalUsuarios= User.objects.count()#cuenta la cantidad de usuarios registrados
    totalBootcamps = Bootcamp.objects.count()#cuenta la cantidad de cursos Bootcamps
    totalInscripciones= BootcampInscripcion.objects.count()#cuenta la cantidad de inscripciones
    
    return render(request, "campus/home_campus.html",{'totalUsuarios':totalUsuarios,'totalBootcamps':totalBootcamps,
                            'totalInscripciones':totalInscripciones,"totalNotificaciones":totalNotificaciones,"emisores":emisores})

def mis_bootcamp(request):
    id_usuario = request.user.id
    usuario_id = get_object_or_404(User, pk=id_usuario)
       
    try:
        emisores = Notificaciones.objects.filter(usuario_receptor=usuario_id.pk).order_by('-created_at')[:5]
        totalNotificaciones= Notificaciones.objects.filter(usuario_receptor=usuario_id.pk).count()#cuenta la cantidad de Mensajes
        bootcampBd = BootcampInscripcion.objects.filter(usuario=usuario_id.pk).order_by('id')
    except BootcampInscripcion.DoesNotExist:
        messages.error(request, "No hay información")
    else: 
        return render(request, "campus/mis_bootcamp.html",{"bootcampBd":bootcampBd,"emisores":emisores,"totalNotificaciones":totalNotificaciones})

def calendario(request):
    id_usuario = request.user.id
    usuario_id = get_object_or_404(User, pk=id_usuario)
       
    try:
        emisores = Notificaciones.objects.filter(usuario_receptor=usuario_id.pk).order_by('-created_at')[:5]
        totalNotificaciones= Notificaciones.objects.filter(usuario_receptor=usuario_id.pk).count()#cuenta la cantidad de Mensajes
        eventosBd = EventosBootcamp.objects.filter(usuario=usuario_id.pk).order_by('id')
    except BootcampInscripcion.DoesNotExist:
        messages.error(request, "No hay información")
    else: 
        return render(request, "campus/calendario.html",{"eventosBd":eventosBd,"emisores":emisores,"totalNotificaciones":totalNotificaciones})

def agregar_evento(request):
    id_usuario = request.user.id
    usuario_id = get_object_or_404(User, pk=id_usuario)
    form = AddEventoForm()    
    
    if request.user.is_authenticated:                

        if request.method == 'POST':
            form = AddEventoForm(request.POST) 
            
            if form.is_valid():
                titulo = request.POST.get("titulo")
                color = request.POST.get("colorpicker-default")
                fecha_inicio = form.cleaned_data['fecha_inicio']
                fecha_fin = form.cleaned_data['fecha_fin']
                 
                evento = EventosBootcamp()

                evento.usuario = usuario_id
                evento.titulo  = titulo
                evento.color_evento = color
                evento.fecha_inicio = fecha_inicio
                evento.fecha_fin = fecha_fin

                evento.save()     #guarda la notificacion en la bd
                messages.success(request, "Evento creado correctamente!!") 
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                messages.error(request, "Datos incorrectos")

        return render(request, "campus/add_evento.html",{"form":form,"usuario_id":usuario_id})
    else:
        return redirect("Iniciar_Sesion")
    
def editar_evento(request,id_evento):

    id_usuario = request.user.id
    usuario_id = get_object_or_404(User, pk=id_usuario)
    evento_id = get_object_or_404(EventosBootcamp, pk=id_evento)
    fecha_inicio = evento_id.fecha_inicio
    fecha_fin = evento_id.fecha_fin
    color_evento = evento_id.color_evento

    if request.user.is_authenticated:
        data = {
            'form': EditEventoForm(instance=evento_id),
            'color_evento':color_evento,
            'evento_id':evento_id,
            'fecha_inicio':fecha_inicio,
            'fecha_fin':fecha_fin,
        }                                 

        if request.method == 'POST':            
            form = EditEventoForm(data=request.POST,instance= evento_id)            
            if form.is_valid():
                titulo = request.POST.get("titulo")
                color = request.POST.get("colorpicker-default")
                fecha_inicio = request.POST.get('id_fecha_inicio')
                fecha_fin = request.POST.get('id_fecha_fin')
                print(fecha_fin)
                evento_id.usuario = usuario_id
                evento_id.titulo  = titulo
                evento_id.color_evento = color
                evento_id.fecha_inicio = fecha_inicio
                evento_id.fecha_fin = fecha_fin

                evento_id.save()                
                form.save()            
                messages.success(request, "Evento actualizado correctamente!!") 
                return redirect(request.META.get('HTTP_REFERER')) 
            else:
                messages.error(request, "Datos incorrectos")
        
        return render(request, "campus/edit_evento.html",data)
    else:
        return redirect("Iniciar_Sesion")

def borrar_evento(request,id_evento):
    evento = get_object_or_404(EventosBootcamp, pk=id_evento)
    evento.delete()
    messages.success(request, "Evento eliminado correctamente!!") 
    return redirect(request.META.get('HTTP_REFERER')) 

def contenido_bootcamp(request,id_bootcamp):
    fecha_actual = datetime.today()   
    
    id_usuario = request.user.id
    usuario_id = get_object_or_404(User, pk=id_usuario)
    id_estudiante = BootcampInscripcion.objects.filter(usuario=usuario_id,bootcamp=id_bootcamp)    
    aprobados = BootcampInscripcion.objects.filter(bootcamp=id_bootcamp)#Filtramos tabla de inscripcion por bootcamp
    asistencia = AssistBootcamp.objects.filter(info_usuario__bootcamp=id_bootcamp).order_by('fecha_clase')

    #Primero se valida que el usuario (Estudiante o empresa) pertenezca al bootcamp
    if id_estudiante:        
        
        try:        
            emisores = Notificaciones.objects.filter(usuario_receptor=usuario_id.pk).order_by('-created_at')[:5]
            totalNotificaciones= Notificaciones.objects.filter(usuario_receptor=usuario_id.pk).count()#cuenta la cantidad de Mensajes
            curso = get_object_or_404(Bootcamp, id=id_bootcamp)            
            lista_estudiantes = BootcampInscripcion.objects.filter(bootcamp=id_bootcamp)
            clases = SesionBootcamp.objects.filter(bootcamp_id = id_bootcamp).order_by('id')    
            entregas = EntregasBootcamp.objects.filter(usuario_id = usuario_id.pk, asignacion_id__sesion_id__bootcamp_id=id_bootcamp)
            tareas = AsignacionBootcamp.objects.filter(sesion_id__bootcamp_id=id_bootcamp)
            gestion_notas = EntregasBootcamp.objects.filter(asignacion_id__sesion_id__bootcamp_id=id_bootcamp)
            
            #Calcula el promedio de la columna calificaciones filtrada por usuario y bootcamp
            promedio_notas = NotasBootcamp.objects.filter(entrega_id__usuario_id = usuario_id.pk,entrega_id__asignacion_id__sesion_id__bootcamp_id=id_bootcamp).aggregate(Avg('calificacion'))
            
            if promedio_notas.get('calificacion__avg') is None:
                nota_final= (0.00)              
            else:   
                nota_final= round(promedio_notas.get('calificacion__avg'),2)                                

        except BootcampInscripcion.DoesNotExist:
            messages.error(request, "No hay información")
        else:
            return render(request, "campus/contenido_bootcamp.html",{"id_bootcamp":id_bootcamp,"curso":curso, "certificado":id_estudiante,
                                    "lista_estudiantes":lista_estudiantes,"emisores":emisores,"totalNotificaciones":totalNotificaciones,
                                    "clases":clases,"entregas":entregas,"nota_final":nota_final,"gestion_notas":gestion_notas,"tareas":tareas,
                                    "asistencia":asistencia,"fecha_actual":fecha_actual})
    else:
        messages.error(request, "No estás inscrito en este Bootcamp o no existe")
        return redirect("Mis_bootcamp")

def notificaciones_bootcamp(request, id_emisor,id_receptor):  

    emisor_id = get_object_or_404(User, pk=id_emisor) 
    receptor_id = get_object_or_404(User, pk=id_receptor)
    mensajes = Notificaciones.objects.filter(usuario_emisor = receptor_id.pk, usuario_receptor = emisor_id.pk)
    form = notificacionForm()    
    
    if request.user.is_authenticated:                

        if request.method == 'POST':
            form = notificacionForm(request.POST) 
            
            if form.is_valid():
                mensaje = request.POST.get("mensaje")                
                n = Notificaciones()

                n.usuario_emisor  = emisor_id
                n.usuario_receptor = id_receptor
                n.mensaje = mensaje

                n.save()     #guarda la notificacion en la bd
                #messages.success(request, "Mensaje enviado satisfactoriamente!!") 
                #return redirect(request.META.get('HTTP_REFERER'))
            else:
                messages.error(request, "Datos incorrectos")

        return render(request, "campus/notificacion.html",{"form":form,"emisor_id":emisor_id,"receptor_id":receptor_id,
                                                           "mensajes":mensajes})
    else:
        return redirect("Iniciar_Sesion")

def borrar_mensaje(request,id_notificacion):
    notificacion = get_object_or_404(Notificaciones, pk=id_notificacion)
    notificacion.delete()
    messages.success(request, "Mensaje eliminado!!") 
    return redirect(request.META.get('HTTP_REFERER')) 
     
def cargar_archivos(request):
    if request.user.is_authenticated :
        if request.method == "POST" and request.FILES['miArchivo']:
            miArchivo = request.FILES['miArchivo']
            fs = FileSystemStorage()
            archivo = fs.save(miArchivo.name, miArchivo)
            carga_archivo_url = fs.url(archivo)
            return render(request, "campus/archivos.html",{
                'carga_archivo_url': carga_archivo_url
            })
        return render(request, "campus/archivos.html")
    
def agregar_clase(request,id_bootcamp):
    id_usuario = request.user.id
    usuario_id = get_object_or_404(User, pk=id_usuario)
    bootcamp_id = get_object_or_404(Bootcamp, pk=id_bootcamp)
    form = AddClaseForm()    
    
    if request.user.is_authenticated:                

        if request.method == 'POST':
            form = AddClaseForm(request.POST) 
            
            if form.is_valid():
                titulo = request.POST.get("titulo")
                contenido = request.POST.get("contenido")
                
                clase = SesionBootcamp()

                clase.titulo  = titulo
                clase.contenido = contenido
                clase.bootcamp = bootcamp_id

                clase.save()     #guarda la notificacion en la bd
                messages.success(request, "Clase añadida correctamente!!") 
                return redirect(request.META.get('HTTP_REFERER'))
                #return redirect("/campus/contenido/"+str(id_bootcamp)+"/")
            else:
                messages.error(request, "Datos incorrectos")

        return render(request, "campus/add_clase.html",{"form":form,"usuario_id":usuario_id,"bootcamp_id":bootcamp_id})
    else:
        return redirect("Iniciar_Sesion")
    
def editar_clase(request,id_clase):
    id_usuario = request.user.id
    usuario_id = get_object_or_404(User, pk=id_usuario)
    clase = get_object_or_404(SesionBootcamp, pk=id_clase)

    if request.user.is_authenticated:
        data = {
            'form': EditClaseForm(instance=clase),
            'usuario_id':usuario_id,
            'clase':clase,
        }                                 

        if request.method == 'POST':            
            form = EditClaseForm(data=request.POST,instance= clase)            
            if form.is_valid():               
                form.save()            
                messages.success(request, "Clase actualizada correctamente!!")
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                messages.error(request, "Datos incorrectos")
        
        return render(request, "campus/edit_clase.html",data)
    else:
        return redirect("Iniciar_Sesion")

def borrar_clase(request,id_clase):
    clase = get_object_or_404(SesionBootcamp, pk=id_clase)
    clase.delete()
    messages.success(request, "Clase eliminada correctamente!!") 
    return redirect(request.META.get('HTTP_REFERER')) 

def agregar_recurso(request,id_clase):

    id_usuario = request.user.id
    usuario_id = get_object_or_404(User, pk=id_usuario)
    clase_id = get_object_or_404(SesionBootcamp, pk=id_clase)
    form = AddRecursoForm()    
    
    if request.user.is_authenticated:                

        if request.method == 'POST':
            form = AddRecursoForm(request.POST,request.FILES)            

            if form.is_valid():                
                titulo = request.POST.get("titulo")
                contenido = request.POST.get("contenido")
                archivo = request.FILES['upload']

                recurso = RecursoBootcamp()

                recurso.titulo  = titulo
                recurso.contenido = contenido
                recurso.upload = archivo
                recurso.sesion = clase_id
                recurso.save()     #guarda la notificacion en la bd
                messages.success(request, "Recurso añadido correctamente!!") 
                return redirect(request.META.get('HTTP_REFERER')) 
            else:
                messages.error(request, "Datos incorrectos")
        return render(request, "campus/add_recurso.html",{"form":form,"usuario_id":usuario_id,"clase_id":clase_id})
    else:
        return redirect("Iniciar_Sesion")

def editar_recurso(request,id_recurso):

    id_usuario = request.user.id
    usuario_id = get_object_or_404(User, pk=id_usuario)
    recurso = get_object_or_404(RecursoBootcamp, pk=id_recurso)

    if request.user.is_authenticated:
        data = {
            'form': EditRecursoForm(instance=recurso),
            'usuario_id':usuario_id,
            'recurso':recurso,
        }           

        if request.method == 'POST':
            form = EditRecursoForm(data=request.POST,instance= recurso,files=request.FILES)            
            if form.is_valid():               
                form.save()            
                messages.success(request, "Recurso actualizado correctamente!!") 
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                messages.error(request, "Datos incorrectos")
        return render(request, "campus/edit_recurso.html",data)
    else:
        return redirect("Iniciar_Sesion")

def borrar_recurso(request,id_recurso):
    recurso = get_object_or_404(RecursoBootcamp, pk=id_recurso)
    recurso.delete()
    messages.success(request, "Recurso eliminado correctamente!!") 
    return redirect(request.META.get('HTTP_REFERER')) 

def agregar_asignacion(request,id_clase):

    id_usuario = request.user.id
    usuario_id = get_object_or_404(User, pk=id_usuario)
    clase_id = get_object_or_404(SesionBootcamp, pk=id_clase)
    form = AddAsginacionForm()    
    
    if request.user.is_authenticated:                

        if request.method == 'POST':
            form = AddAsginacionForm(request.POST,request.FILES) 

            if form.is_valid():                
                titulo = request.POST.get("titulo")
                contenido = request.POST.get("contenido")
                archivo = request.FILES['upload']

                asig = AsignacionBootcamp()

                asig.titulo  = titulo
                asig.contenido = contenido
                asig.upload = archivo
                asig.sesion = clase_id
                asig.save()     #guarda la notificacion en la bd
                messages.success(request, "Asignación añadida correctamente!!") 
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                messages.error(request, "Datos incorrectos")
        return render(request, "campus/add_asignacion.html",{"form":form,"usuario_id":usuario_id,"clase_id":clase_id})
    else:
        return redirect("Iniciar_Sesion")

def editar_asignacion(request,id_asignacion):

    id_usuario = request.user.id
    usuario_id = get_object_or_404(User, pk=id_usuario)
    asignacion = get_object_or_404(AsignacionBootcamp, pk=id_asignacion)

    if request.user.is_authenticated:
        data = {
            'form': EditAsignacionForm(instance=asignacion),
            'usuario_id':usuario_id,
            'asignacion':asignacion,
        }           

        if request.method == 'POST':
            form = EditAsignacionForm(data=request.POST,instance= asignacion,files=request.FILES)            
            if form.is_valid():               
                form.save()             
                messages.success(request, "Asignación actualizada correctamente!!") 
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                messages.error(request, "Datos incorrectos")
        return render(request, "campus/edit_asignacion.html", data)
    else:
        return redirect("Iniciar_Sesion")

def borrar_asignacion(request,id_asignacion):
    asignacion = get_object_or_404(AsignacionBootcamp, pk=id_asignacion)
    asignacion.delete()
    messages.success(request, "Asignación eliminada correctamente!!") 
    return redirect(request.META.get('HTTP_REFERER')) 

def agregar_entrega(request,id_asignacion):
    
    id_usuario = request.user.id
    usuario_id = get_object_or_404(User, pk=id_usuario)
    asignacion_id = get_object_or_404(AsignacionBootcamp, pk=id_asignacion)
    form = AddEntregaForm()    
    
    if request.user.is_authenticated:                

        if request.method == 'POST':
            form = AddEntregaForm(request.POST,request.FILES) 

            if form.is_valid():                
                archivo = request.FILES['upload']

                entreg = EntregasBootcamp()

                entreg.usuario = usuario_id
                entreg.asignacion = asignacion_id
                entreg.upload = archivo
                
                entreg.save()     #guarda la notificacion en la bd
                messages.success(request, "Entrega enviada correctamente!!") 
                return redirect(request.META.get('HTTP_REFERER')) 
            else:
                messages.error(request, "Datos incorrectos")
        return render(request, "campus/add_entrega.html",{"form":form,"usuario_id":usuario_id,"asignacion_id":asignacion_id})
    else:
        return redirect("Iniciar_Sesion")

def editar_entrega(request,id_entrega):

    id_usuario = request.user.id
    usuario_id = get_object_or_404(User, pk=id_usuario)
    entrega_id = get_object_or_404(EntregasBootcamp, pk=id_entrega)

    if request.user.is_authenticated:
        data = {
            'form': EditEntregaForm(instance=entrega_id),
            'usuario_id':usuario_id,
            'entrega_id':entrega_id,
        }           

        if request.method == 'POST':
            form = EditEntregaForm(data=request.POST,instance= entrega_id,files=request.FILES)            
            if form.is_valid():               
                form.save()             
                messages.success(request, "Entrega Actualizada correctamente!!") 
                return redirect(request.META.get('HTTP_REFERER')) 
            else:
                messages.error(request, "Datos incorrectos")
        return render(request, "campus/edit_entrega.html", data)
    else:
        return redirect("Iniciar_Sesion")

def agregar_nota(request,id_entrega):

    id_usuario = request.user.id
    usuario_id = get_object_or_404(User, pk=id_usuario)
    entrega_id = get_object_or_404(EntregasBootcamp, pk=id_entrega)

    form = AddNotaForm()    
    
    if request.user.is_authenticated:                

        if request.method == 'POST':
            form = AddNotaForm(request.POST)            

            if form.is_valid():
                
                comentario = request.POST.get("comentario")
                calificacion = request.POST.get("calificacion")

                nota = NotasBootcamp()

                nota.comentario  = comentario
                nota.calificacion = calificacion                
                nota.entrega = entrega_id
                nota.save()     #guarda la notificacion en la bd
                messages.success(request, "Calificación añadida correctamente!!") 
                return redirect(request.META.get('HTTP_REFERER')) 
            else:
                messages.error(request, "Datos incorrectos")
        return render(request, "campus/add_nota.html",{"form":form,"usuario_id":usuario_id,"entrega_id":entrega_id})
    else:
        return redirect("Iniciar_Sesion")

def editar_nota(request,id_nota):

    id_usuario = request.user.id
    usuario_id = get_object_or_404(User, pk=id_usuario)
    nota = get_object_or_404(NotasBootcamp, pk=id_nota)

    if request.user.is_authenticated:
        data = {
            'form': EditNotaForm(instance=nota),
            'usuario_id':usuario_id,
            'nota':nota,
        }           

        if request.method == 'POST':
            form = EditNotaForm(data=request.POST,instance= nota)            
            if form.is_valid():               
                form.save()    
                messages.success(request, "Calificación actualizada correctamente!!") 
                return redirect(request.META.get('HTTP_REFERER')) 
            else:
                messages.error(request, "Datos incorrectos")
        return render(request, "campus/edit_nota.html",data)
    else:
        return redirect("Iniciar_Sesion")

def editar_perfil(request):

    id_usuario = request.user.id
    usuario = get_object_or_404(User, pk=id_usuario)
    usuario_id = get_object_or_404(userProfile, pk=id_usuario)
    if request.user.is_authenticated:
        data = {
            'form': EditPerfilForm(instance=usuario_id),
            'usuario_id':usuario_id,
            'usuario':usuario,
        }     

        if request.method == "POST":
            form = EditPerfilForm(data=request.POST,instance= usuario_id,files=request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, "Información Actualizada!!") 
                return redirect(request.META.get('HTTP_REFERER'))   
            else:
                messages.error(request, "Datos incorrectos")  
        return render(request, "campus/edit_perfil.html",data)
    else:
        return redirect("Iniciar_Sesion")                      

def certificado(request,id_bootcamp):
    id_usuario = request.user.id
    usuario_id = get_object_or_404(User, pk=id_usuario)
    id_estudiante = BootcampInscripcion.objects.filter(usuario=usuario_id,bootcamp=id_bootcamp)    

    #obtenemos la fecha actual y le damos formato YYYY-mm-dd
    fecha_actual = date.today()     
       
    try:
        curso = get_object_or_404(Bootcamp, id=id_bootcamp)
        emisores = Notificaciones.objects.filter(usuario_receptor=usuario_id.pk).order_by('-created_at')[:5]
        totalNotificaciones= Notificaciones.objects.filter(usuario_receptor=usuario_id.pk).count()#cuenta la cantidad de Mensajes
        bootcampBd = BootcampInscripcion.objects.filter(usuario=usuario_id.pk).order_by('id')
    except BootcampInscripcion.DoesNotExist:
        messages.error(request, "No hay información")
    else: 
        return render(request, "campus/certificado.html",{"usuario_id":usuario_id,"curso":curso,"bootcampBd":bootcampBd,
                                                          "emisores":emisores,"totalNotificaciones":totalNotificaciones,"fecha_actual":fecha_actual})
     
def asistencia_bootcamp(request,id_bootcamp):

    #obtenemos la fecha actual y le damos formato YYYY-mm-dd
    fecha_actual = datetime.today()
    fecha_seleccionada = ''
    assistances = AssistBootcamp.objects.none()

    id_usuario = request.user.id
    usuario_id = get_object_or_404(User, pk=id_usuario)
    id_estudiante = BootcampInscripcion.objects.filter(bootcamp=id_bootcamp)
    curso = get_object_or_404(Bootcamp, id=id_bootcamp)
    emisores = Notificaciones.objects.filter(usuario_receptor=usuario_id.pk).order_by('-created_at')[:5]
    totalNotificaciones= Notificaciones.objects.filter(usuario_receptor=usuario_id.pk).count()#cuenta la cantidad de Mensajes

    #Primero se valida que el usuario (Estudiante o empresa) pertenezca al bootcamp
    if id_estudiante: 

        if request.method == 'GET':
            fecha_seleccionada = request.GET.get('fecha', '')
            if fecha_seleccionada:
                try:
                    fecha_seleccionada = datetime.strptime(fecha_seleccionada, '%Y-%m-%d').date()
                    assistances = AssistBootcamp.objects.filter(fecha_clase__date=fecha_seleccionada)
                    if not assistances.exists() and not AssistBootcamp.objects.filter(fecha_clase=fecha_seleccionada).exists():
                        # Crear una nueva lista de asistencia
                        bootcamp = get_object_or_404(Bootcamp, id=id_bootcamp)
                        inscripciones = BootcampInscripcion.objects.filter(bootcamp=bootcamp)
                        new_assistances = []
                        for inscripcion in inscripciones:
                            assistance = AssistBootcamp(fecha_clase=fecha_seleccionada)
                            assistance.save()
                            assistance.info_usuario.set([inscripcion])
                            new_assistances.append(assistance)
                        AssistBootcamp.objects.bulk_create(new_assistances, ignore_conflicts=True)

                except ValueError:
                    pass

        if request.method == 'POST':
            assistances_ids = request.POST.getlist('asistencia_ids')
            assistances_values = request.POST.getlist('asistencia_values')

            for assistance_id, assistance_value in zip(assistances_ids, assistances_values):
                assistance = AssistBootcamp.objects.get(id=assistance_id)
                assistance.asistencia = assistance_value.split('-')[1] == 'True'
                assistance.save()
            return redirect('Asistencia_bootcamp', id_bootcamp=id_bootcamp)        
          
        context = {
            'assistances': assistances,
            'fecha_actual' : fecha_actual,
            'fecha_seleccionada': fecha_seleccionada.strftime('%Y-%m-%d') if fecha_seleccionada else '',
            'id_bootcamp': id_bootcamp,
            "curso" : curso,
            "emisores" : emisores,
            "totalNotificaciones": totalNotificaciones,
        } 

        return render(request, "campus/asistencia_bootcamp.html", context)
    
    else:
          messages.error(request, "No estás inscrito en este Bootcamp o no existe")
          return redirect("Mis_bootcamp")
    
def notas_bootcamp(request,id_bootcamp):
    fecha_actual = datetime.today()   
    
    id_usuario = request.user.id
    usuario_id = get_object_or_404(User, pk=id_usuario)
    id_estudiante = BootcampInscripcion.objects.filter(usuario=usuario_id,bootcamp=id_bootcamp)    
    aprobados = BootcampInscripcion.objects.filter(bootcamp=id_bootcamp)#Filtramos tabla de inscripcion por bootcamp
    asistencia = AssistBootcamp.objects.filter(info_usuario__bootcamp=id_bootcamp).order_by('fecha_clase')

    #Primero se valida que el usuario (Estudiante o empresa) pertenezca al bootcamp
    if id_estudiante:       
        
        try:        
            emisores = Notificaciones.objects.filter(usuario_receptor=usuario_id.pk).order_by('-created_at')[:5]
            totalNotificaciones= Notificaciones.objects.filter(usuario_receptor=usuario_id.pk).count()#cuenta la cantidad de Mensajes
            curso = get_object_or_404(Bootcamp, id=id_bootcamp)            
            lista_estudiantes = BootcampInscripcion.objects.filter(bootcamp=id_bootcamp)
            clases = SesionBootcamp.objects.filter(bootcamp_id = id_bootcamp).order_by('id')    
            entregas = EntregasBootcamp.objects.filter(usuario_id = usuario_id.pk, asignacion_id__sesion_id__bootcamp_id=id_bootcamp)
            tareas = AsignacionBootcamp.objects.filter(sesion_id__bootcamp_id=id_bootcamp)
            gestion_notas = EntregasBootcamp.objects.filter(asignacion_id__sesion_id__bootcamp_id=id_bootcamp)
            
            #Calcula el promedio de la columna calificaciones filtrada por usuario y bootcamp
            promedio_notas = NotasBootcamp.objects.filter(entrega_id__usuario_id = usuario_id.pk,entrega_id__asignacion_id__sesion_id__bootcamp_id=id_bootcamp).aggregate(Avg('calificacion'))
            
            if promedio_notas.get('calificacion__avg') is None:
                nota_final= (0.00)              
            else:   
                nota_final= round(promedio_notas.get('calificacion__avg'),2)                                

        except BootcampInscripcion.DoesNotExist:
            messages.error(request, "No hay información")
        else:
            return render(request, "campus/notas_bootcamp.html",{"id_bootcamp":id_bootcamp,"curso":curso, "certificado":id_estudiante,
                                    "lista_estudiantes":lista_estudiantes,"emisores":emisores,"totalNotificaciones":totalNotificaciones,
                                    "clases":clases,"entregas":entregas,"nota_final":nota_final,"gestion_notas":gestion_notas,"tareas":tareas,
                                    "asistencia":asistencia,"fecha_actual":fecha_actual})
    else:
        messages.error(request, "No estás inscrito en este Bootcamp o no existe")
        return redirect("Mis_bootcamp")

def calcular_promedios_calificaciones(student_ids, id_bootcamp):
    promedio_notas = NotasBootcamp.objects.filter(
        entrega_id__usuario_id__in=student_ids,
        entrega_id__asignacion_id__sesion_id__bootcamp_id=id_bootcamp
    ).values('entrega_id__usuario_id').annotate(Avg('calificacion'))

    for promedio in promedio_notas:
        usuario_id = promedio['entrega_id__usuario_id']
        calificacion_promedio = round(promedio['calificacion__avg'], 2)

        prom, created = PromedioBootcamp.objects.get_or_create(datos_id=usuario_id)
        prom.promedio = calificacion_promedio
        prom.save()

def seleccion_estudiante(request, id_bootcamp):
    fecha_actual = datetime.today()

    id_usuario = request.user.id
    usuario_id = get_object_or_404(User, pk=id_usuario)
    id_estudiante = BootcampInscripcion.objects.filter(usuario=usuario_id, bootcamp=id_bootcamp)
    student_ids = BootcampInscripcion.objects.filter(bootcamp=id_bootcamp).values_list('usuario_id', flat=True)
    aprobados = BootcampInscripcion.objects.filter(bootcamp=id_bootcamp)
    asistencia = AssistBootcamp.objects.filter(info_usuario__bootcamp=id_bootcamp).order_by('fecha_clase')

    # Primero se valida que el usuario (Estudiante o empresa) pertenezca al bootcamp
    if id_estudiante:
        if "boxes" in request.POST:
            id_list = request.POST.getlist('boxes')
            # uncheck all inscripciones
            aprobados.update(status=False)
            for x in id_list:
                BootcampInscripcion.objects.filter(pk=int(x)).update(status=True)

        try:
            emisores = Notificaciones.objects.filter(usuario_receptor=usuario_id.pk).order_by('-created_at')[:5]
            totalNotificaciones = Notificaciones.objects.filter(usuario_receptor=usuario_id.pk).count()
            curso = get_object_or_404(Bootcamp, id=id_bootcamp)
            lista_estudiantes = BootcampInscripcion.objects.filter(bootcamp=id_bootcamp)
            clases = SesionBootcamp.objects.filter(bootcamp_id=id_bootcamp).order_by('id')
            entregas = EntregasBootcamp.objects.filter(usuario_id=usuario_id.pk, asignacion_id__sesion_id__bootcamp_id=id_bootcamp)
            tareas = AsignacionBootcamp.objects.filter(sesion_id__bootcamp_id=id_bootcamp)
            gestion_notas = EntregasBootcamp.objects.filter(asignacion_id__sesion_id__bootcamp_id=id_bootcamp)

            calcular_promedios_calificaciones(student_ids, id_bootcamp)

        except BootcampInscripcion.DoesNotExist:
            messages.error(request, "No hay información")
        else:
            return render(request, "campus/seleccion_estudiante.html", {"id_bootcamp": id_bootcamp, "curso": curso, "certificado": id_estudiante,
                                                                         "lista_estudiantes": lista_estudiantes, "emisores": emisores, "totalNotificaciones": totalNotificaciones,
                                                                         "clases": clases, "entregas": entregas, "gestion_notas": gestion_notas, "tareas": tareas,
                                                                         "asistencia": asistencia, "fecha_actual": fecha_actual})
    else:
        messages.error(request, "No estás inscrito en este Bootcamp o no existe")
        return redirect("Mis_bootcamp")

def bootcamp_report(request, id_bootcamp):
    id_usuario = request.user.id
    usuario_id = get_object_or_404(User, pk=id_usuario)
    bootcamp = Bootcamp.objects.get(id=id_bootcamp)
    estudiantes = BootcampInscripcion.objects.filter(bootcamp=bootcamp)
    emisores = Notificaciones.objects.filter(usuario_receptor=usuario_id.pk).order_by('-created_at')[:5]
    totalNotificaciones = Notificaciones.objects.filter(usuario_receptor=usuario_id.pk).count()
    curso = get_object_or_404(Bootcamp, id=id_bootcamp)
    reporte = []
    aprobados = 0
    reprobados = 0
    for estudiante in estudiantes:
        promedios = PromedioBootcamp.objects.filter(datos=estudiante)
        if promedios.exists():
            promedio = promedios.first().promedio
        else:
            promedio = 0.0
        if estudiante.status:
            resultado = "Aprobado"
            aprobados += 1            
        else:
            resultado = "Reprobado"
            reprobados += 1        

        reporte.append({
            "estudiante": estudiante,
            "promedio": promedio,
            "resultado": resultado
        })
    
    total_estudiantes= aprobados+reprobados
    porcentaje_apro = round((aprobados / total_estudiantes) * 100)
    porcentaje_repro = round((reprobados / total_estudiantes) * 100)

    # Datos para el gráfico
    labels = ["Aprobados", "Reprobados"]
    data = [aprobados, reprobados] 
    
    context = {
        "bootcamp": bootcamp,
        "reporte": reporte,
        "labels": labels,
        "data": data,
        "curso": curso,
        "emisores": emisores,
        "totalNotificaciones":totalNotificaciones,
        "porcentaje_apro":porcentaje_apro,
        "porcentaje_repro":porcentaje_repro
    }
    return render(request, "campus/bootcamp_report.html", context)

 




