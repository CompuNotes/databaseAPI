from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import User, Tag, Rating, File

admin.site.register(User)
admin.site.register(Tag)
admin.site.register(Rating)
admin.site.register(File)