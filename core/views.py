from django.shortcuts import render
from .models import HomeView

# Create your views here.
def home(request):
    home = HomeView.objects.all()
    return render (request, "core/home.html", {'home':home})