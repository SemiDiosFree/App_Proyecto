from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver

# Create your models here.
class Categorias(models.Model):
    tag = models.CharField(verbose_name='Categoría', max_length=50)

    class Meta: 
        verbose_name="Etiqueta"

    def __str__(self):
        return self.tag

def upload_location(instance, filename):
    return "%s/%s" %(instance.tag, filename)

class Repositorio(models.Model):
    tag = models.ForeignKey(Categorias,verbose_name='Etiqueta', on_delete=models.CASCADE)
    image = models.FileField(upload_to=upload_location)

    class Meta:
        verbose_name='Repositorio de imágenes'

class Imagenes(models.Model):
    tag = models.ForeignKey(Categorias,verbose_name='Etiqueta', null=True, blank=True, on_delete=models.CASCADE)
    proyecto = models.ForeignKey('Proyectos', verbose_name='idProyecto', blank=True, null=True, on_delete=models.SET_NULL)
    image = models.ImageField(upload_to=upload_location, null=True, blank=True)

    class Meta: 
        verbose_name="Imágenes"

@receiver(post_delete, sender = Imagenes)
def image_delete(sender, instance, **kwargs):
    #Borrar los ficheros de las fotos que se eliminan.
    instance.image.delete(False)

class FotoTrampa(models.Model):
    token = models.AutoField(primary_key=True)
    ipaddress = models.GenericIPAddressField(protocol='both', unpack_ipv4=True , null=True, blank=True,max_length=15, verbose_name='Dirección IP')
    #mask = models.GenericIPAddressField(protocol='both', unpack_ipv4=True , null=True, blank=True,max_length=15, verbose_name='Máscara de red')
    domain = models.URLField(null=True, blank=True, max_length=200,verbose_name='Dominio')
    #img = models.ImageField(upload_to = "photTramp/", null = True, blank = True)

    class Meta:
        verbose_name = "Foto-Trampa"
        verbose_name_plural = "Foto-Trampas"
        ordering = ['ipaddress']

    def __str__(self):
        return self.ipaddress

class Proyectos(models.Model):
    id = models.AutoField(primary_key=True)
    FKauthor = models.ForeignKey(User, verbose_name='Autor', on_delete=models.CASCADE)
    FKFT = models.ForeignKey(FotoTrampa, verbose_name='Foto-Trampa', blank=True, null=True, on_delete=models.SET_NULL)
    MTMIMG = models.ManyToManyField(Imagenes,verbose_name='Imágenes',blank=True, related_name='+')
    title = models.CharField(verbose_name="Título", max_length=200)
    content = models.TextField(verbose_name="Descripción")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    class Meta: 
        verbose_name="Proyecto"

    def __str__(self):
        return self.title

class Historial(models.Model):
    idUser = models.ForeignKey(User, null=True, blank=True, verbose_name="Usuario", on_delete=models.CASCADE)
    idProjecto = models.ForeignKey(Proyectos, null=True, blank=True, verbose_name="Projecto", on_delete=models.CASCADE)
    idPhotoTramp = models.ForeignKey(FotoTrampa, null=True, blank=True, verbose_name="Foto-trampa", on_delete=models.CASCADE)
    idImages = models.ForeignKey(Imagenes, null=True, blank=True, verbose_name="Imagen", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Historial"