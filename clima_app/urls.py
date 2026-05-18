# agro_app/urls.py
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('datos/', views.vista_datos, name='vista_datos'),
    path('alertas/', views.panel_alertas, name='panel_alertas'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Nueva ruta para el formulario de registro público
    path('registro/', views.registro_usuario, name='registro'),
    
    # 🔥 NUEVAS RUTAS PARA EL CRUD DE REGISTROS (CONTROLADAS POR ESCALA)
    path('datos/nuevo/<str:escala>/', views.crear_registro, name='crear_registro'),
    path('datos/editar/<str:escala>/<int:pk>/', views.editar_registro, name='editar_registro'),
    path('datos/eliminar/<str:escala>/<int:pk>/', views.eliminar_registro, name='eliminar_registro'),
]