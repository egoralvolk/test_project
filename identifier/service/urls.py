from django.urls import path, include
from service import views

urlpatterns = [
    path('', views.index),
    path('person', views.persons),
]
