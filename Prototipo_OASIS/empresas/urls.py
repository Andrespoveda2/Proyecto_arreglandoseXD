from django.urls import path
from . import views

app_name = 'empresas'  # Para namespace

urlpatterns = [
    # --- Dashboard y perfil ---
    path('dashboard/', views.dashboard_empresa, name='dashboard_empresa'),
    path('editar_perfil/', views.editar_perfil_empresa, name='editar_perfil_empresa'),
    path('perfil/', views.Perfil_Empresa, name='mi_perfil_empresa'),

    # --- Proyectos ---
    path('crear_proyecto/', views.crear_proyecto, name='crear_proyecto'),
    path('editar_proyecto/<int:pk>/', views.editar_proyecto, name='editar_proyecto'),
    path('proyecto/<int:pk>/', views.detalle_proyecto_empresa, name='detalle_proyecto_empresa'),  # ✅ NUEVA RUTA
    path('proyecto/<int:pk>/postulaciones/', views.postulaciones_proyecto, name='postulaciones_proyecto'),

    # --- Postulaciones de aprendices ---
    path('postulacion/<int:postulacion_id>/<str:accion>/', views.gestionar_postulacion, name='gestionar_postulacion'),

    # --- Postulaciones de instructores ---
    path(
        'postulacion_instructor/<int:postulacion_id>/<str:accion>/',
        views.gestionar_postulacion_instructor,
        name='gestionar_postulacion_instructor'
    ),
]
