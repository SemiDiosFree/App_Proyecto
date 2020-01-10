from django import forms
from .models import Proyectos, Imagenes, Repositorio
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