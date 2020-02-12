from django.urls import path

from simplemooc.courses import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('details/<int:pk>', views.details, name='details'),
    path('details/<str:slug>', views.details, name='details'),
    path('enrollment/<str:slug>', views.enrollment, name='enrollment'),
]
