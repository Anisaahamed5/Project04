from django.urls import path
from . import views

urlpatterns = [
    path('home.html', view.home, name="home")
]