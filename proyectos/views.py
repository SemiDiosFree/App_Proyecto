from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.urls import reverse, reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormView
from .forms import PageForm, ImageForm, MultipleImageForm
from .models import Proyectos, Imagenes, Historial, Repositorio, Categorias
from django.contrib.auth.models import User
from .services import extract_features, training, clasification
from django.shortcuts import render
import sys, os
from django.http import HttpResponseRedirect
from django.contrib import messages
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
    paginate_by = 15
    model = Proyectos
    ruta = os.getcwd()+'\\'
    print('La ruta es: ',ruta)
    #Obtiene todas las imágenes que se agregan
    
    def get_context_data(self, **kwargs):
        #   Añadir un if
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        titulo = context.get('proyectos')
        print(titulo)
        #   Añadir un if
        for i in Imagenes.objects.all():
            print('Imagenes: ',i.proyecto)
        print('2    ************-')
        context['img']=Imagenes.objects.filter(proyecto = titulo)
        print('CTX: ',context)
        print('Nombre del proyecto: ',self.kwargs.get('slug'))
        return context

 #CreateView Project#
@method_decorator(login_required, name='dispatch')
class ProjectViewCreate(CreateView):
    model = Proyectos
    form_class = PageForm
    success_url = reverse_lazy('projects:projects')

    def post(self,request):
        form_class = PageForm
        if request.method == 'POST':
            form = PageForm(request.POST)
            if form.is_valid():
                title = str(form.cleaned_data['title'])
                ruta = os.path.abspath('media')+'\\'
                print('Ruta donde se guardaran: ',ruta)
                #comprobar si la ruta existe
                if os.path.isdir(ruta+title):
                    print('La carpeta ya existe')
                else:
                    os.mkdir(ruta+title)
                    print('se creo!!')
                    ruta = os.path.abspath('media'+'\\'+title)
                    print('Ruta del proyecto: ',ruta)
                    messages.success(request, 'Creado.')

                    model = '\\'+'models'
                    print('modelo: ',model)
                    os.mkdir(ruta+model)
                    print('se creo el modelo')
                    media = '\\'+'media'
                    os.mkdir(ruta+media)
                    print('se creo la carpeta media')
                    
                    
            return self.form_valid(form)
        return self.form_invalid(form)

    

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
                #FM = form.save(commit=False)
                #form.save()
                FM.save()
                for f in files:
                    gallery = Repositorio(tag = FM, image=f)
                    gallery.save()
                return self.form_valid(form)
                extract()
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
