from django import forms
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import ValidationError


class RegisterForm(forms.Form):
	username = forms.CharField(label="Nombre de Usuario",widget=forms.TextInput(attrs={'required': True,'type':"text", 'class':"fs-13px",'placeholder':'Ingrese un usuario valido'}))
	email = forms.EmailField(label="Correo Electrónico",widget=forms.TextInput(attrs={'type':"text",'class':"fs-13px",'placeholder':'Ingrese su correo electrónico'}))
	password_one = forms.CharField(label="Contraseña",widget=forms.PasswordInput(render_value=False, attrs={'required': True,'class':"fs-13px",'placeholder':'Ingrese su contraseña'}))
	password_two = forms.CharField(label="Confirmar Contraseña",widget=forms.PasswordInput(render_value=False, attrs={'trequired': True,'class':"fs-13px",'placeholder':"Confirme Contraseña"}))
	
	#validar si el usuario ya existe
	def clean_username(self):
		username = self.cleaned_data['username']
		try:
			u = User.objects.get(username=username)
		except User.DoesNotExist:
			return username #para que valide el formulario como si fuera correcto
		raise ValidationError("Nombre de usuario existente")
		
	#validar si ya existe el correo 
	def clean_email(self):
		email = self.cleaned_data['email']
		try:
			u = User.objects.get(email=email)
		except User.DoesNotExist:
			return email #para que valide el formulario como si fuera correcto
		raise forms.ValidationError('Correo existente')

	#validar que el password coincida y tenga mínimo 8 caracteres, minisculas y mayusculas
	def clean_password_two(self):
		password_one = self.cleaned_data['password_one']
		password_two = self.cleaned_data['password_two']
		espacio=False
		mayuscula=False #variable para identificar letras mayúsculas
		minuscula=False #variable para contar identificar letras minúsculas
		numeros=False
        
		for carac in password_one :
			if carac.isspace()==True: #Saber si el caracter es un espacio
				espacio=True #si encuentra un espacio se cambia el valor user
			#if carac.isupper()== True: #saber si hay mayuscula
			#	mayuscula=True #acumulador o contador de mayusculas
			if carac.islower()== True: #saber si hay minúsculas
				minuscula=True #acumulador o contador de minúsculas
			if carac.isdigit()== True: #saber si hay números
				numeros=True #acumulador o contador de numeros
                    
		if espacio==True:
			raise forms.ValidationError('La contraseña no puede contener espacios en blanco')
			
		if len(password_one) < 5 :
			raise forms.ValidationError('La contraseña debe tener mínimo 8 caracteres')

		if minuscula ==True and numeros == True :
			pass
		else:
			raise forms.ValidationError('La contraseña elegida no es segura: debe contener letras y números')
			
		if password_one == password_two:
			pass
		else:
			raise forms.ValidationError('Contraseñas no coinciden')