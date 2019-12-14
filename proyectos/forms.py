from django import forms
from .models import Proyectos, Imagenes, FotoTrampa, Repositorio
from django.http import HttpResponse


class PageForm(forms.ModelForm):

    class Meta:
        model = Proyectos
        fields = ['title', 'content','FKauthor']
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Titulo'}),
            'content': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Contenido'}),
            
            #'author': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Autor'}),
        }

        labels = {
            'title':'', 'content':'', 'author':'Autor'
        }
        

class MultipleImageForm(forms.ModelForm):
    class Meta:
        model = Repositorio
        fields = ['tag', 'image']
        widgets = { 
            'image': forms.ClearableFileInput(attrs={'class':'form-control', 'multiple':True})
        }

        labels = {
            'Repositorio de imágenes': 'image'
        }

class ImageForm(forms.ModelForm):
    class Meta:
        model = Imagenes
        fields = ['proyecto','image']
        widgets = {
            'image':forms.ClearableFileInput(attrs={'class':'form-control-file mt-3'}),
        }

        labels = {
            'IDProyecto':'', 'image':'Imágen'
        }
class PhotoTrampForm(forms.ModelForm):
    class Meta:
        model = FotoTrampa
        #Agregar la etiqueta de mask en fields
        fields = ['ipaddress','domain']
        widgets = {
            'ipaddress':forms.NumberInput(attrs={'class':'form-control-file mt-3'}),
            #'mask':forms.NumberInput(attrs={'class':'form-control-file mt-3'}),
            'domain' : forms.URLInput(attrs={'class':'form-control-file mt-3'})
        }

        labels = {
            'ipaddress':'IP', 'domain':'Nombre de dominio'
        }