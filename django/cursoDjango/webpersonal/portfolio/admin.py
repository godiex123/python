from django.contrib import admin
from .models import Project

# Register your models here.
class ProjectAdmin(admin.ModelAdmin):
    readonly_fields = ("created", "updated") # Extendiendo la funcionalidad de Django para mostrar los campos que django-admin oculta pero solo como readonly

admin.site.register(Project, ProjectAdmin) # Para que se vea en el panel de admin, agregamos la extension