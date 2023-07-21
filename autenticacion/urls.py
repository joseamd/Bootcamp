from django.urls import path
from .views import cerrar_sesion, loguear, registro
from django.contrib.auth import views as auth_views

urlpatterns = [
    #path('', VRegistro.as_view(), name="Autenticacion"),
    path('cerrar_sesion', cerrar_sesion, name="Cerrar_Sesion"),
    path('iniciar_sesion', loguear, name="Iniciar_Sesion"),
    path('registro', registro, name="Autenticacion"),
    # vistas del reset del password
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name = "recuperarPassword/reset_password.html"), name ='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name = "recuperarPassword/password_reset_done.html"), name ='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name = "recuperarPassword/password_reset_confirm.html"), name ='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = "recuperarPassword/password_reset_complete.html"), name ='password_reset_complete'),
]