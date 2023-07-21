from django import forms
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import ValidationError
from campus.models import *
from autenticacion.models import *
import requests
from django.forms.widgets import NumberInput
from django.forms import TextInput, DateInput, DateTimeInput

class notificacionForm(forms.Form):

    mensaje = forms.CharField(label='',widget=forms.Textarea(attrs={'required': True,'type':"text", 'rows':"6", 'cols':"60",'class':"form-control",'placeholder':"Escribe un mensaje..."}))

class AddClaseForm(forms.Form):

    titulo = forms.CharField(label='* Titulo',widget=forms.TextInput(attrs={'required': True,'type':"text", 'class':"form-control"}))
    contenido = forms.CharField(label='* Contenido',widget=forms.TextInput(attrs={'required': True,'type':"text", 'class':"form-control"}))
    
class AddRecursoForm(forms.Form):

    titulo = forms.CharField(label='* Titulo',widget=forms.TextInput(attrs={'required': True,'type':"text", 'class':"form-control"}))
    contenido = forms.CharField(label='* Contenido',widget=forms.TextInput(attrs={'required': True,'type':"text", 'class':"form-control"}))
    upload = forms.FileField(label='* Archivo',widget=forms.FileInput(attrs={'required': True,'type':"file"}))

class AddAsginacionForm(forms.Form):

    titulo = forms.CharField(label='* Titulo',widget=forms.TextInput(attrs={'required': True,'type':"text", 'class':"form-control"}))
    contenido = forms.CharField(label='* Contenido',widget=forms.TextInput(attrs={'required': True,'type':"text", 'class':"form-control"}))
    upload = forms.FileField(label='* Archivo',widget=forms.FileInput(attrs={'required': True,'type':"file"}))

class AddNotaForm(forms.Form):

    comentario = forms.CharField(label='* Comentario',widget=forms.TextInput(attrs={'required': True,'type':"text", 'class':"form-control"}))
    calificacion = forms.CharField(label='* Calificación',widget=forms.NumberInput(attrs={'required': True,'min':0.0,'max':5.0,'step': "0.01"}))

class AddEntregaForm(forms.Form):

    upload = forms.FileField(label='* Archivo',widget=forms.FileInput(attrs={'required': True,'type':"file"}))

class EditClaseForm(forms.ModelForm):    

    class Meta:
        model = SesionBootcamp
        
        fields = ["titulo","contenido"]
        widgets = {
            'titulo': TextInput(attrs={'required': True,'type':'text','class':"form-control"}),
            'contenido': TextInput(attrs={'required': True,'type':'text','class':"form-control"}),
        }

class EditRecursoForm(forms.ModelForm):    

    class Meta:
        model = RecursoBootcamp
        
        fields = ["titulo","contenido","upload"]
        widgets = {
            'titulo': TextInput(attrs={'required': True,'type':'text','class':"form-control"}),
            'contenido': TextInput(attrs={'required': True,'type':'text','class':"form-control"}),
        }

class EditAsignacionForm(forms.ModelForm):    

    class Meta:
        model = AsignacionBootcamp
        
        fields = ["titulo","contenido","upload"]
        widgets = {
            'titulo': TextInput(attrs={'required': True,'type':'text','class':"form-control"}),
            'contenido': TextInput(attrs={'required': True,'type':'text','class':"form-control"}),
        }

class EditNotaForm(forms.ModelForm):    

    class Meta:
        model = NotasBootcamp
        
        fields = ["comentario","calificacion"]
        widgets = {
            'comentario': TextInput(attrs={'required': True,'type':'text','class':"form-control"}),
            'calificacion': NumberInput(attrs={'required': True,'min':0.0,'max':5.0,'step': "0.01"}),
        }

class EditEntregaForm(forms.ModelForm):    

    class Meta:
        model = EntregasBootcamp        
        fields = ["upload"]
        
class EditPerfilForm(forms.ModelForm):
        
    class Meta:
        model = userProfile
        
        fields = ["photo","e_mail"]
        widgets = {
            'Correo': TextInput(attrs={'type':"text",'class':"fs-13px",'placeholder':'Ingrese su correo electrónico'}),
        }

class AddEventoForm(forms.Form):

    titulo = forms.CharField(label='* Evento',widget=forms.TextInput(attrs={'required': True,'type':"text", 'class':"form-control"}))
    fecha_inicio = forms.DateTimeField(label="* Fecha de inicio", required=True, widget=NumberInput(attrs={'type':'date','class':"form-control"}))
    fecha_fin = forms.DateTimeField(label="* Fecha de finalización", required=True, widget=NumberInput(attrs={'type':'date','class':"form-control"}))
    
class EditEventoForm(forms.ModelForm):    

    class Meta:
        model = EventosBootcamp
        
        fields = ["titulo"]
        widgets = {
            'titulo': TextInput(attrs={'required': True,'type':'text','class':"form-control"}),                        
        }
