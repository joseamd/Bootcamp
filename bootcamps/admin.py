from django.contrib import admin
from .models import Tipo_Categoria, Bootcamp, ProgramasAcademico, BootcampInscripcion

# Register your models here.

class Tipo_CategoriaAdmin(admin.ModelAdmin):    
    readonly_fields= ('created', 'update')

class BootcampAdmin(admin.ModelAdmin):
    list_display =('id', 'titulo')
    readonly_fields= ('created', 'update')

class BootcampInscripcioncampAdmin(admin.ModelAdmin):
    list_display =('cedula','nombre','apellido')
    search_fields=("cedula","apellido","bootcamp")
    readonly_fields= ('created', 'update')

class ProgramasAcademicoAdmin(admin.ModelAdmin):
    search_fields=("codigo",)
    list_display =('codigo', 'nombre')


admin.site.register(Tipo_Categoria, Tipo_CategoriaAdmin)
admin.site.register(Bootcamp, BootcampAdmin)
admin.site.register(ProgramasAcademico, ProgramasAcademicoAdmin)
admin.site.register(BootcampInscripcion, BootcampInscripcioncampAdmin)