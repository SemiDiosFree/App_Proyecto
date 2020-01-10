from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver
import os
# Create your models here.
class Categorias(models.Model):
    tag = models.CharField(verbose_name='Categoría', max_length=50)

    class Meta: 
        verbose_name="Etiqueta"

    def __str__(self):
        return self.tag

class Categorias2(models.Model):
    tag = models.CharField(verbose_name='Categoría', max_length=50)

    class Meta: 
        verbose_name="Etiquetado"

    def __str__(self):
        return self.tag

def upload_location(instance, filename):
    return "%s/%s" %(instance.tag, filename)

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return '{0}/media/{1}/'.format(instance.proyecto.tag, filename)

class Repositorio(models.Model):
    tag = models.ForeignKey(Categorias,verbose_name='Etiqueta', on_delete=models.CASCADE)
    image = models.FileField(upload_to=upload_location)
    proyecto = models.ForeignKey('Proyectos', verbose_name='idProyecto', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name='Repositorio de imágenes'

    def __str__(self):
        return "%s/%s" %(self.tag, self.id)

class Imagenes(models.Model):
    tag = models.ForeignKey(Categorias2,verbose_name='Etiqueta', null=True, blank=True, on_delete=models.CASCADE)
    proyecto = models.ForeignKey('Proyectos', verbose_name='idProyecto', blank=True, null=True, on_delete=models.SET_NULL)
    image = models.ImageField(upload_to=upload_location, null=True, blank=True)

    class Meta: 
        verbose_name="Imágenes"

    def __str__(self):
        return "%s/%s" %(self.proyecto, self.id)

@receiver(post_delete, sender = Imagenes)
def image_delete(sender, instance, **kwargs):
    #Borrar los ficheros de las fotos que se eliminan.
    instance.image.delete(False)


class Proyectos(models.Model):
    id = models.AutoField(primary_key=True)
    FKauthor = models.ForeignKey(User, verbose_name='Autor', on_delete=models.CASCADE)
    MTMIMG = models.ManyToManyField(Imagenes,verbose_name='Imágenes',blank=True, related_name='+')
    title = models.CharField(verbose_name="Título", max_length=200, unique=True)
    content = models.TextField(verbose_name="Descripción")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")
    tag = models.ForeignKey(Categorias2,verbose_name='Etiqueta', null=True, blank=True, on_delete=models.CASCADE)

    class Meta: 
        verbose_name="Proyecto"

    def __str__(self):
        return self.title


class Historial(models.Model):
    idUser = models.ForeignKey(User, null=True, blank=True, verbose_name="Usuario", on_delete=models.CASCADE)
    idProjecto = models.ForeignKey(Proyectos, null=True, blank=True, verbose_name="Projecto", on_delete=models.CASCADE)
    idImages = models.ForeignKey(Imagenes, null=True, blank=True, verbose_name="Imagen", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Historial"