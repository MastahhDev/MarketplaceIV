from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Producto
from functools import wraps

def usuario_es_creador(view_func):
    @wraps(view_func)
    def wrapper(request, pk, *args, **kwargs):
        producto = get_object_or_404(Producto, pk=pk)
        if producto.usuario != request.user:
            return HttpResponseForbidden("No tienes permiso para realizar esta acción.")
        return view_func(request, pk, *args, **kwargs)
    return wrapper

def registro(request):
    if request.method == 'GET':
        return render(request, 'registro.html', {'form': UserCreationForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('products:lista')  
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
        return render(request, 'login.html', {'form': AuthenticationForm})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'login.html', {
                'form': AuthenticationForm,
                'error': 'El nombre o la contraseña son incorrectos'
            })
        else:
            login(request, user)
            return redirect('products:lista')  

@login_required
def signout(request):
    logout(request)
    return redirect('home')

# Vistas de Productos
def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'products/lista_productos.html', {'productos': productos})

@login_required
def crear_producto(request):
    if request.method == 'POST':
        
        producto = Producto(
            nombre=request.POST.get('nombre'),
            precio=request.POST.get('precio'),
            descripcion=request.POST.get('descripcion'),
            stock=request.POST.get('stock'),
            usuario=request.user  # 👈 NUEVO: Asignar el usuario actual
        )
        
        
        if 'imagen' in request.FILES:
            producto.imagen = request.FILES['imagen']
        
        producto.save()
        return redirect('products:lista')
    
    return render(request, 'products/crear_producto.html')

def detalle_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'products/detalle_producto.html', {'producto': producto})

@login_required
@usuario_es_creador
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    
    if request.method == 'POST':
        producto.nombre = request.POST.get('nombre')
        producto.precio = request.POST.get('precio')
        producto.descripcion = request.POST.get('descripcion')
        producto.stock = request.POST.get('stock')
        
        
        if 'imagen' in request.FILES:
            producto.imagen = request.FILES['imagen']
        
        producto.save()
        return redirect('products:lista')
    
    return render(request, 'products/editar_producto.html', {'producto': producto})
    
    return render(request, 'products/editar_producto.html', {'producto': producto})

@login_required
@usuario_es_creador
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('products:lista')  # ✅ CAMBIADO
    
    return render(request, 'products/eliminar_producto.html', {'producto': producto})