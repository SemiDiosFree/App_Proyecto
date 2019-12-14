from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
class HomeView(models.Model):
    title = models.CharField(verbose_name="Título", max_length=200)
    content = RichTextField(verbose_name="Contenido")
    url = models.URLField(verbose_name="Enlace", max_length=200, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")
    
    class Meta:
        verbose_name = "principal"
        verbose_name_plural = "principales"
        ordering = ['title']

    def __str__(self):
        return self.title