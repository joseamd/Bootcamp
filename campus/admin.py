from django.contrib import admin
from .models import *

# Register your models here.

class NotificacionesAdmin(admin.ModelAdmin):
    search_fields=("usuario_emisor","usuario_receptor")
    list_display =("usuario_emisor","usuario_receptor")
    readonly_fields= ('created_at', 'updated_at')

class SesionBootcampAdmin(admin.ModelAdmin):
    list_display=('id','titulo','bootcamp')
    readonly_fields= ('created_at', 'updated_at')

class RecursoBootcampAdmin(admin.ModelAdmin):
    list_display =('id','titulo')
    readonly_fields= ('created_at', 'updated_at')

class AsignacionBootcampAdmin(admin.ModelAdmin):
    list_display =('id','titulo')
    readonly_fields= ('created_at', 'updated_at')

class EntregasBootcampAdmin(admin.ModelAdmin):
    list_display =('id','usuario', 'asignacion')
    readonly_fields= ('created_at', 'updated_at')

class NotasBootcampAdmin(admin.ModelAdmin):
    list_display =('id','entrega', 'calificacion')
    readonly_fields= ('created_at', 'updated_at')

class EventosBootcampAdmin(admin.ModelAdmin):
    list_display=('id','titulo','fecha_inicio','fecha_fin')
    readonly_fields= ('created_at', 'updated_at')

class AssistBootcampAdmin(admin.ModelAdmin):
    list_display=('id','fecha_clase','asistencia')
    readonly_fields= ('created_at', 'updated_at')

admin.site.register(Notificaciones, NotificacionesAdmin)
admin.site.register(SesionBootcamp, SesionBootcampAdmin)
admin.site.register(RecursoBootcamp, RecursoBootcampAdmin)
admin.site.register(AsignacionBootcamp, AsignacionBootcampAdmin)
admin.site.register(NotasBootcamp, NotasBootcampAdmin)
admin.site.register(EntregasBootcamp, EntregasBootcampAdmin)
admin.site.register(EventosBootcamp, EventosBootcampAdmin)
admin.site.register(AssistBootcamp, AssistBootcampAdmin)
admin.site.register(PromedioBootcamp)
