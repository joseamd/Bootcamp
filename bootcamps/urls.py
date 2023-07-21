from django.urls import path
from bootcamps import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    #path('', views.bootcamps, name="Bootcamp"),
    path('page/<int:pagina>/', views.bootcamps,name='Bootcamp'),
    path('inscripcion/<int:bootcamp_id>/<int:id>/', login_required(views.inscripcion), name="Inscripcion"),
    path('buscar_bootcamp/', views.buscar_bootcamp, name="Buscar_bootcamp"),
    path('add_bootcamp/<int:id>/', login_required(views.add_bootcamp), name="Add_bootcamp"),   
    path('edit_bootcamp/<int:id_bootcamp>/', login_required(views.edit_bootcamp), name="Edit_bootcamp"), 
    path('delete_bootcamp/<int:id_bootcamp>/', login_required(views.delete_bootcamp), name="Delete_bootcamp"),
]