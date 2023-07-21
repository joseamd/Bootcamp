from django.shortcuts import render, redirect
from .forms import formularioContacto
from django.core.mail import EmailMessage
from bootcamps.models import Bootcamp, Tipo_Categoria
from blog.models import Post,Categoria
from django.contrib import messages


# Create your views here.

def contacto(request): 
    categBd= Categoria.objects.all()#Categorías de blog
    blogs = Post.objects.all().order_by('-id')[:5]#Publicaciones o blog Max 5
    tipo_categBd= Tipo_Categoria.objects.all()#categorías de Bootcamp
    formulario_contacto = formularioContacto()
    mensaje=""

    if request.method == "POST":
        formulario_contacto = formularioContacto(data=request.POST)
        if formulario_contacto.is_valid():
            nombre = request.POST.get("nombre")
            email = request.POST.get("email")
            mensaje = request.POST.get("mensaje")

            # email = EmailMessage("Mensaje desde App Django","El usuario con nombre {} con la dirección {} escribe lo siguiente:\n\n {}".format(nombre,email,contenido),"","alexpoison100@gmail.com", reply_to=[email])
            email = EmailMessage(
                'Mensaje desde App Django',
                'El usuario: {}\nCorreo: {}\nMensaje:\n\n{}'.format(nombre,email,mensaje),
                'finishingschool.bootcamp@gmail.com',
                ['finishingschool.bootcamp@gmail.com'],
                reply_to=[email],                
            )
            try:
                email.send()
                messages.success(request, "Información enviada correctamente!!")
                return redirect("/contacto/?valido")
            except:
                return redirect("/contacto/?novalido")


    return render(request, "contacto/contacto.html", {"miFormulario":formulario_contacto,
    "tipo_categBd":tipo_categBd,"blogs":blogs,"categBd":categBd})