from django.urls import path
from simplemooc.core import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contato', views.contato, name='contact'),
    path('about', views.about, name='about'),
]
