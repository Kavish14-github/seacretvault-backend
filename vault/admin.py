from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Project, Environment, Secret

admin.site.register(Project)
admin.site.register(Environment)
admin.site.register(Secret)
