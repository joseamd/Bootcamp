from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import userProfile
from django.contrib.auth.models import User
from .forms import RegisterForm

# Create your views here.

# class VRegistro(View):

#     def get(self, request):
#         form=UserCreationForm()
#         return render(request, "autenticacion/register_v3.html",{"form":form})

#     def post(self, request):
#         form=UserCreationForm(request.POST)
        
#         if form.is_valid():
#             usuario=form.save()
#             login(request, usuario)
#             return redirect("Home")
#         else:
#             for msg in form.error_messages:
#                 messages.error(request, form.error_messages[msg])
#             return render(request, "autenticacion/register_v3.html",{"form":form})

def cerrar_sesion(request):
    logout(request)
    return redirect("Home")

def loguear(request):

    if request.method=="POST":
        form=AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username=form.cleaned_data.get("username")
            password=form.cleaned_data.get("password")
            usuario=authenticate(username=username, password=password)
            if usuario is not None:
                login(request, usuario)
                return redirect("Home")
            else:
                messages.error(request, "Usuario y/o Contraseña son incorrectos")
        else:
            messages.error(request, "Usuario y/o Contraseña son incorrectos")

    form=AuthenticationForm()
    return render(request, "autenticacion/login_v3.html",{"form":form})

def registro(request):
    
	form = RegisterForm()
	if request.method == "POST":
		form = RegisterForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			email = form.cleaned_data['email']
			password_one = form.cleaned_data['password_one']
			password_two = form.cleaned_data['password_two']
			u = User.objects.create_user(username=username, email=email, password=password_one)
			u.save()#guarda el usuario
			return render(request,'autenticacion/gracias_registro.html')		

	return render(request,'autenticacion/register_v3.html', {"form":form})