from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from products import views

def home(request):
    return render(request,'home.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('products/', views.products, name='products'),
    path('register/', views.registro, name='register'),
    path('login/', views.signin, name='login'),
    path('logout/', views.signout, name='logout'),
]
