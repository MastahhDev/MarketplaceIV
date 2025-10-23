from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate

# Create your views here.
def registro(request):
    if request.method == 'GET':
        return render(request, 'registro.html', {
        'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            # registrar el usuario
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('products')
            except:
                return render(request, 'registro.html', {
                'form': UserCreationForm,
                'error': 'El usuario ya existe'
                })
        return render(request, 'registro.html', {
                'form': UserCreationForm,
                'error': 'Las contraseñas no coinciden'
                })
    
def signin(request):
    if request.method == 'GET':
        return render(request, 'login.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'login.html', {
                'form': AuthenticationForm,
                'error': 'El nombre o la contraseña son incorrectos'
            })
        else:
            login(request, user)
            return redirect('products')
            
def signout(request):
    logout(request)
    return redirect('home')

def products(request):
    return render(request, 'products/products.html')