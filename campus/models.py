from django.db import models
from bootcamps.models import *
from django.contrib.auth.models import User
from crum import get_current_user


# Create your models here.


class SesionBootcamp(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.CharField(max_length=500)
    bootcamp = models.ForeignKey(Bootcamp, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "seccionBootcamp"
        verbose_name_plural = "seccionBootcampS"
    
    def __str__(self):
        return self.titulo

class RecursoBootcamp(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.CharField(max_length=500)
    upload = models.FileField(upload_to='campus/cargas/')
    sesion = models.ForeignKey(SesionBootcamp, on_delete=models.CASCADE, related_name="recurso")  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "RecursoBootcamp"
        verbose_name_plural = "RecursoBootcamps"
    
    def __str__(self):
        return self.titulo

class AsignacionBootcamp(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.CharField(max_length=500)
    upload = models.FileField(upload_to='campus/asignaciones/')
    sesion = models.ForeignKey(SesionBootcamp, on_delete=models.CASCADE, related_name="asignacion")  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "AsignacionBootcamp"
        verbose_name_plural = "AsignacionBootcamps"
    
    def __str__(self):
        return self.titulo
    
class EntregasBootcamp(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    asignacion = models.ForeignKey(AsignacionBootcamp, on_delete=models.CASCADE, related_name="entrega")
    upload = models.FileField(upload_to='campus/entregas/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "EntregasBootcamp"
        verbose_name_plural = "EntregasBootcamps"    

class NotasBootcamp(models.Model):
    entrega = models.ForeignKey(EntregasBootcamp, on_delete=models.CASCADE, related_name="nota") 
    comentario = models.CharField(max_length=500)
    calificacion = models.FloatField(blank=True, null=True, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "NotasBootcamp"
        verbose_name_plural = "NotasBootcamps"
    
class Notificaciones(models.Model):
    usuario_emisor = models.ForeignKey(User, on_delete=models.CASCADE)
    usuario_receptor = models.IntegerField(blank=True, null=True)
    mensaje = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "NotificacionesBootcamp"
        verbose_name_plural = "NotificacionesBootcamps"
    
    def __str__(self):
        return self.mensaje
    
class EventosBootcamp(models.Model):
    titulo = models.CharField(max_length=500)
    color_evento = models.CharField(max_length=500)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "EventosBootcamp"
        verbose_name_plural = "EventosBootcamps"

    def __str__(self):
        return self.titulo

class AssistBootcamp(models.Model):
    info_usuario = models.ManyToManyField(BootcampInscripcion, related_name="assist")
    fecha_clase = models.DateTimeField(blank=True)
    asistencia = models.BooleanField('Assist',default=False)            
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "AssistBootcamp"
        verbose_name_plural = "AssistBootcamps"
    
    def __date__(self):
        return self.fecha_clase

class PromedioBootcamp(models.Model):
    datos = models.ForeignKey(BootcampInscripcion, on_delete=models.CASCADE, related_name="prom_inscripcion") 
    promedio = models.FloatField(blank=True, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "PromedioBootcamp"
        verbose_name_plural = "PromedioBootcamps"
