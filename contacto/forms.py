from django import forms


class formularioContacto(forms.Form):

    nombre = forms.CharField(label="Nombre ", required=True, max_length=100, widget=forms.TextInput(attrs={'type':"text", 'class':"form-control"}))    
    email = forms.CharField(label="Email ", required=True, widget=forms.TextInput(attrs={'type':"text", 'class':"form-control"}))
    mensaje = forms.CharField(label="Mensaje ", max_length=300, widget=forms.Textarea(attrs={'type':"text", 'class':"form-control"}))