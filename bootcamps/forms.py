from django import forms
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import ValidationError
from bootcamps.models import *
import requests
from django.forms.widgets import NumberInput
from django.forms import TextInput, DateInput, SelectMultiple


class AddBootcampForm(forms.Form):

    titulo = forms.CharField(label='* Titulo',widget=forms.TextInput(attrs={'required': True,'type':"text", 'class':"form-control"}))
    contenido = forms.CharField(label='* Contenido',widget=forms.TextInput(attrs={'required': True,'type':"text", 'class':"form-control"}))
    imagen = forms.ImageField(label='* Imagen',widget=forms.FileInput(attrs={'required': True,'type':"file"}))
    requisito1 = forms.CharField(label='* Requisito1',widget=forms.TextInput(attrs={'required': True,'type':"text", 'class':"form-control"}))
    requisito2 = forms.CharField(label='Requisito2',widget=forms.TextInput(attrs={'required': False,'type':"text", 'class':"form-control"}))
    requisito3 = forms.CharField(label='Requisito3',widget=forms.TextInput(attrs={'required': False,'type':"text", 'class':"form-control"}))
    requisito4 = forms.CharField(label='Requisito4',widget=forms.TextInput(attrs={'required': False,'type':"text", 'class':"form-control"}))
    requisito5 = forms.CharField(label='Requisito5',widget=forms.TextInput(attrs={'required': False,'type':"text", 'class':"form-control"}))
    categoria = forms.ModelChoiceField(label='* Categoría',widget=forms.Select(attrs={'required': True,'class':"form-control"}), queryset=Tipo_Categoria.objects.all().order_by('-id'),empty_label="Seleccione la categoría")
    fecha_inicio = forms.DateTimeField(label="* Fecha de inicio", required=True, widget=NumberInput(attrs={'type':'date','class':"form-control"}))

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        # asi vuelves tus campos no requeridos
        self.fields['requisito2'].required = False
        self.fields['requisito3'].required = False
        self.fields['requisito4'].required = False
        self.fields['requisito5'].required = False
    
    
class EditBootcampForm(forms.ModelForm):    

    class Meta:
        model = Bootcamp
        
        fields = ["titulo","contenido","imagen","requisito1","requisito2","requisito3","requisito4",
                   "requisito5","categoria"]
        #fields = '__all__'
        widgets = {
            'titulo': TextInput(attrs={'required': True,'type':'text','class':"form-control"}),
            'contenido': TextInput(attrs={'required': True,'type':'text','class':"form-control"}),
            'requisito1': TextInput(attrs={'required': True,'type':'text','class':"form-control"}),
            'requisito2': TextInput(attrs={'required': False,'type':'text','class':"form-control"}),
            'requisito3': TextInput(attrs={'required': False,'type':'text','class':"form-control"}),
            'requisito4': TextInput(attrs={'required': False,'type':'text','class':"form-control"}),
            'requisito4': TextInput(attrs={'required': False,'type':'text','class':"form-control"}),
            'requisito5': TextInput(attrs={'required': False,'type':'text','class':"form-control"}),
            'categoria': SelectMultiple(attrs={'required': True,'class':"form-control"}),
            #'fecha_inicio': DateInput(attrs={'class':"form-control"}),
        }