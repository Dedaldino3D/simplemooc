from django.contrib.auth.decorators import login_required
from django.shortcuts import render


# Create your views here.


def home(request):
    template_name = 'home.html'
    return render(request, template_name)


def contato(request):
    template_name = 'contato.html'
    return render(request, template_name)


def about(request):
    template_name = 'about.html'
    return render(request, template_name)
