from django.urls import path

from . import views

urlpatterns = [
    path('index', views.index, name='index'),

    # authentication
    path('register', views.Register),
    path('login', views.Login),
    path('addproduct', views.AddProduct),

    ]