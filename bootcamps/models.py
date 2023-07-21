from django.db import models
from django.contrib.auth.models import User
from .services import enviar_datos_microservicio
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Tipo_Categoria(models.Model):
    nombre      = models.CharField(max_length=100)
    created     = models.DateTimeField(auto_now_add=True)
    update      = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Tipo_categoria"
        verbose_name_plural = "Tipo_categorias"
    
    def __str__(self):
        return self.nombre

class Bootcamp(models.Model):

    titulo      = models.CharField(max_length=200)
    contenido   = models.CharField(max_length=500)
    imagen      = models.ImageField(upload_to='bootcamps')
    requisito1   = models.CharField(max_length=100)
    requisito2   = models.CharField(max_length=100, blank=True)
    requisito3   = models.CharField(max_length=100, blank=True)
    requisito4   = models.CharField(max_length=100, blank=True)
    requisito5   = models.CharField(max_length=100, blank=True)
    autor       = models.ForeignKey(User, on_delete=models.CASCADE)
    categoria   = models.ManyToManyField(Tipo_Categoria)
    fecha_inicio = models.DateTimeField()
    created     = models.DateTimeField(auto_now_add=True)
    update      = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "bootcamp"
        verbose_name_plural = "bootcamps"
    
    def __str__(self):
        return self.titulo


class ProgramasAcademico(models.Model):

	codigo		= models.BigIntegerField(null=False, unique=True, primary_key=True)
	nombre		= models.CharField(max_length=100)	
	status		= models.BooleanField(default=True)

	def __str__(self):
		return '%s - %s' % (self.codigo, self.nombre) 

class BootcampInscripcion(models.Model):

    cedula		= models.IntegerField(blank=True, null=True)  
    nombre		= models.CharField(max_length=100)
    apellido	= models.CharField(max_length=100)
    usuario     = models.ForeignKey(User, on_delete=models.CASCADE)
    carrera		= models.ManyToManyField(ProgramasAcademico)
    email		= models.EmailField(max_length=254)
    direccion   = models.CharField(max_length=100)
    telefono    = models.CharField(max_length=10)
    bootcamp    = models.ManyToManyField(Bootcamp, related_name="bootcamp")
    created     = models.DateTimeField(auto_now_add=True)
    update      = models.DateTimeField(auto_now_add=True)
    status		= models.BooleanField('Aprroved',default=False)

    class Meta:
        verbose_name = "BootcampInscripcion"
        verbose_name_plural = "BootcampInscripciones"

    def __str__(self):
        bootcamps = ", ".join(str(seg) for seg in self.bootcamp.all())
        return '%s - %s - %s' % (self.cedula, self.nombre, bootcamps)

    def save(self, *args, **kwargs):
        if self.pk:
            original_status = BootcampInscripcion.objects.get(pk=self.pk).status
            if not original_status and self.status:
                enviar_datos_microservicio(self.usuario.id, self.bootcamp.first().titulo)
        super().save(*args, **kwargs)


@receiver(post_save, sender=BootcampInscripcion)
def enviar_datos_si_finalizado(sender, instance, created, **kwargs):
    if instance.status and created:
        estudiante_id = instance.usuario.id
        bootcamp = instance.bootcamp.first().titulo
        enviar_datos_microservicio(estudiante_id, bootcamp)


