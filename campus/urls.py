from django.urls import path
from campus import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('', login_required(views.campus), name="Campus"),
    path('mis_bootcamp/', login_required(views.mis_bootcamp), name="Mis_bootcamp"),
    path('calendario/', login_required(views.calendario), name="Calendario"),
    path('add_evento/', login_required(views.agregar_evento), name="Add_evento"),
    path('edit_evento/<int:id_evento>/', login_required(views.editar_evento), name="Edit_evento"),
    path('delete_evento/<int:id_evento>/', login_required(views.borrar_evento), name="Borrar_evento"),
    path('contenido/<int:id_bootcamp>/', login_required(views.contenido_bootcamp), name="Contenido_bootcamp"),
    path('asistencia/<int:id_bootcamp>/', login_required(views.asistencia_bootcamp), name="Asistencia_bootcamp"),
    path('reporte/<int:id_bootcamp>/', login_required(views.bootcamp_report), name="Bootcamp_report"),
    path('notas/<int:id_bootcamp>/', login_required(views.notas_bootcamp), name="Notas_bootcamp"),
    path('seleccion/<int:id_bootcamp>/', login_required(views.seleccion_estudiante), name="Seleccion_estudiante"),
    path('notificacion/<int:id_emisor>/<int:id_receptor>/', login_required(views.notificaciones_bootcamp), name="Notificaciones_bootcamp"),
    path('delete_notificacion/<int:id_notificacion>/', login_required(views.borrar_mensaje), name="Borrar_notificacion"),
    path('archivos/', views.cargar_archivos, name="ArchivosCampus"),
    path('add_clase/<int:id_bootcamp>/', login_required(views.agregar_clase), name="Add_clase"),
    path('edit_clase/<int:id_clase>/', login_required(views.editar_clase), name="Edit_clase"),
    path('delete_clase/<int:id_clase>/', login_required(views.borrar_clase), name="Borrar_clase"),
    path('add_recurso/<int:id_clase>/', login_required(views.agregar_recurso), name="Add_recurso"),
    path('edit_recurso/<int:id_recurso>/', login_required(views.editar_recurso), name="Edit_recurso"),
    path('delete_recurso/<int:id_recurso>/', login_required(views.borrar_recurso), name="Borrar_recurso"),
    path('add_asignacion/<int:id_clase>/', login_required(views.agregar_asignacion), name="Add_asignacion"),
    path('edit_asignacion/<int:id_asignacion>/', login_required(views.editar_asignacion), name="Edit_asignacion"),
    path('delete_asignacion/<int:id_asignacion>/', login_required(views.borrar_asignacion), name="Borrar_asignacion"),
    path('add_nota/<int:id_entrega>/', login_required(views.agregar_nota), name="Add_nota"),
    path('edit_nota/<int:id_nota>/', login_required(views.editar_nota), name="Edit_nota"),
    path('add_entrega/<int:id_asignacion>/', login_required(views.agregar_entrega), name="Add_entrega"),
    path('edit_entrega/<int:id_entrega>/', login_required(views.editar_entrega), name="Edit_entrega"),
    path('certificado_bootcamp/<int:id_bootcamp>/', login_required(views.certificado), name="Certificado_bootcamp"),
    path('edit_perfil/', login_required(views.editar_perfil), name="Edit_perfil"),
]