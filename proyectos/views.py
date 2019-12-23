from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.urls import reverse, reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormView
from .forms import PageForm, ImageForm, PhotoTrampForm, MultipleImageForm
from .models import Proyectos, Imagenes, Historial, Repositorio, Categorias
from django.contrib.auth.models import User
from .services import extract_features, training, clasification
from django.shortcuts import render
import sys
from django.http import HttpResponseRedirect

from .services import extract_features
from subprocess import run, PIPE
from django.core.files.storage import FileSystemStorage
from django.http import Http404
from django.http import HttpResponse
from django.views import View
from django.shortcuts import render, get_object_or_404

# Create your views here.
    
    #ListView Project#
@method_decorator(login_required, name='dispatch')
class ProjectListView(ListView):
    model = Proyectos
    #filtrar a los proyectos por autor
    def get_queryset(self):
        return Proyectos.objects.filter(FKauthor = self.request.user)

    ##DetailView Project
@method_decorator(login_required, name='dispatch')
class ProjectDetailView(DetailView):
    model = Proyectos

    #Obtiene todas las imágenes que se agregan
    def get_context_data(self, **kwargs):
        for i in Imagenes.objects.all():
            print('Modelo Imagenes: ',i.proyecto)
        for p in Proyectos.objects.all():
            print('modelo Proyecto: ', p.title)
        context = super().get_context_data(**kwargs)
        context['img']=Imagenes.objects.filter(proyecto = i.proyecto)
        print('Modelo Proyecto: ',context)
        
        #extract_features()
        return context
    
    #filtrar a las imagenes por id del proyecto
    #def get_queryset(self):
     #   return Imagenes.objects.filter(proyecto__title=str(Proyectos.title))

 #CreateView Project#
@method_decorator(login_required, name='dispatch')
class ProjectViewCreate(CreateView):
    model = Proyectos
    form_class = PageForm
    success_url = reverse_lazy('projects:projects')

    def dispatch(self, request, *args, **kwargs):
                    # Imprimimos el usuario que inicio sesión 
        print(request.user)

        return super().dispatch(request, *args, **kwargs)

##UpdateView Project
@method_decorator(login_required, name='dispatch')
class ProjectViewUpdate(UpdateView):
    model = Proyectos
    form_class = PageForm
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('projects:projects') 
    #def get_success_url(self):
        #return reverse_lazy('projects:update', args=[self.object.id]) 

#DeletView Projec
@method_decorator(login_required, name='dispatch')
class ProjectViewDelete(DeleteView):
    model = Proyectos
    success_url = reverse_lazy('projects:projects') 

#Add Images Project
@method_decorator(login_required, name='dispatch')
class AddImagesView(LoginRequiredMixin, CreateView):        # Agregar imagenes a la base de datos solamente
    model = Imagenes
    form_class = ImageForm
    success_url = reverse_lazy('projects:projects')
    

#Add Repos Images Project
@method_decorator(login_required, name='dispatch')
class RepositorioImagesView(LoginRequiredMixin, CreateView):        # Add Images
    model = Repositorio
    form_class = MultipleImageForm
    success_url = reverse_lazy('projects:projects')

    def post(self, request):
        form_class = MultipleImageForm
        #form = self.get_form(form_class)
        if request.method == 'POST':
            form= MultipleImageForm(request.POST, request.FILES)
            files = request.FILES.getlist('image')
            if form.is_valid():
                FM = Categorias(tag = str(form.cleaned_data['tag']))
                #str(form.save(commit=False))
                #form.save()
                FM.save()
                for f in files:
                    gallery = Repositorio(tag = FM, image=f)
                    gallery.save()
                return self.form_valid(form)
            else:
                return self.form_invalid(form)

#funcion donde está agregado el metodo de extracción de características
def extract(request):
    extract_features()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

#funcion donde está agregado el metodo de entrenamiento
def script(request):
    training()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

#funcion donde está agregado el metodo clasificación
def clasifi(request):
    clasification()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
