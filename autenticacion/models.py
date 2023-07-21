from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe


# Create your models here.

class userProfile(models.Model):

    def url(self, filename):
        ruta ="MultimediaData/Users/%s/%s"%(self.user.username,filename)
        return ruta

    def user_imagen(self):
        return mark_safe('<img src="{}" width="20" />'.format(self.photo.url))

    user_imagen.allow_tags = True

    user 		= models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    photo		= models.ImageField(default='MultimediaData/Users/Default/user-default.png',upload_to=url)
    e_mail		= models.EmailField(max_length=254)

    def __str__(self):
        return self.user.username
