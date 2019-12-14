from django.urls import path
from .views import *

projects_patterns = ([
    path('', ProjectListView.as_view(), name="projects"),
    path('<int:pk>/<slug:slug>/', ProjectDetailView.as_view(), name="project"),
    path('create/', ProjectViewCreate.as_view(), name="create"),
    path('update/<int:pk>/', ProjectViewUpdate.as_view(), name="update"),
    path('delete/<int:pk>/', ProjectViewDelete.as_view(), name="delete"),
    path('imagesAdd/', AddImagesView.as_view(), name="imagesAdd"),
    path('repos/', RepositorioImagesView.as_view(), name="repos"),
    path('training/', script, name='entrenamiento'),
    path('clasifi/', clasifi, name='clasificacion'),
   # path('phototramp/', PTListView.as_view(), name="phototramp"),
],'projects')
