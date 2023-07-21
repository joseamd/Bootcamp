from django.contrib import admin
from .models import userProfile

# Register your models here.

class userProfileAdmin(admin.ModelAdmin):
    list_display =('user', 'user_imagen', 'e_mail')
    list_filter = ('user', 'e_mail')
    search_fields = ('user', 'e_mail')

admin.site.register(userProfile, userProfileAdmin)