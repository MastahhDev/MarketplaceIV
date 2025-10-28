from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from products import views  # ✅ Importa views completo
from django.conf import settings
from django.conf.urls.static import static

def home(request):
    return render(request, 'home.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('products/', views.lista_productos, name='products'),
    path('register/', views.registro, name='register'),
    path('login/', views.signin, name='login'),
    path('logout/', views.signout, name='logout'),
    
    path('', include('products.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)