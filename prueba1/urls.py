from django.contrib import admin
from django.urls import path, include
from core.urls import core_patterns
from pages.urls import pages_patterns
from django.conf import settings
from proyectos.urls import projects_patterns

urlpatterns = [
    #path de core
    path('',include(core_patterns)),
    #path de pages
    path('page/',include(pages_patterns)),
    #path de auth
    path('accounts/', include('django.contrib.auth.urls')),
    #path de registro
    path('accounts/', include('registration.urls')),
    #path de projects
    path('projects/', include(projects_patterns)),
    #path de Admin
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


"""prueba1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""