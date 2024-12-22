"""
URL configuration for IOTPMV project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tasks import views as tasks_views
from usuarios import views as usuarios_views
from formacion import views as formacion_views
from gestion_instructores import views as gestion_instructores_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Ruta Admin
    path('admin/', admin.site.urls),

    # Ruta default
    path('', usuarios_views.home, name='home'),

    # Registro usuarios
    path('signup/', usuarios_views.signup, name='signup'),

    # Log out
    path('logout/', usuarios_views.signout, name='logout'),

    # Log In
    path('signin/', usuarios_views.signin, name='signin'),

    # CRUD base TASKS:
    path('tasks/', tasks_views.tasksView, name='tasks'),
    path('tasks_completed/', tasks_views.tasks_completed, name='tasks_completed'),
    path('tasks/create/', tasks_views.create_task, name='create_task'),
    path('tasks/<int:task_id>/', tasks_views.task_detail, name='task_detail'),
    path('tasks/<int:task_id>/complete/',
         tasks_views.complete_task, name='complete_task'),
    path('tasks/<int:task_id>/delete/',
         tasks_views.delete_task, name='delete_task'),

    # ROL Admin
    path('admin_dashboard/', usuarios_views.dashboard_admin, name='admin_dashboard'),
    path('aprendices/', usuarios_views.aprendices, name='aprendices'),
    path('instructores/', usuarios_views.instructores, name='instructores'),
    path('instructores/crear/', usuarios_views.crear_instructor,
         name='crear_instructor'),
    path('instructores/<int:instructor_id>/',
         usuarios_views.instructor_detalle, name='instructor_detalle'),
    path('obtener_detalles/<int:instructor_id>/',
         usuarios_views.instructor_detalle_tabla, name='obtener_detalles'),
    path('administradores/', usuarios_views.administradores, name='administradores'),
    path('administradores/crear/',
         usuarios_views.crear_administradores, name='crear_administradores'),
    path('lideres/', usuarios_views.lideres, name='lideres'),
    path('lideres/crear/',
         usuarios_views.lideres, name='crear_lideres'),

    # ROL Instructores
    path('gestion_instructor/', gestion_instructores_views.gestion_instructor,
         name='gestion_instructor'),
    path('get_tree_instructor/', formacion_views.tree_detalle,
         name='get_tree_instructor'),

    # Panel instructor
    path('fichas/', formacion_views.listar_fichas, name='listar_fichas'),
    path('fichas/<int:ficha_id>/', formacion_views.panel_ficha, name='panel_ficha'),
    path('fichas/<int:ficha_id>/crear_actividad/',
         formacion_views.crear_actividad, name='crear_actividad'),


    # ROL Aprendices
    path('panel_aprendiz/', formacion_views.panel_aprendiz, name='panel_aprendiz'),




    # Novedades
    path('novedades/', usuarios_views.novedades, name='novedades'),
    path('novedades/crear/', usuarios_views.crear_novedad, name='crear_novedad'),

    # Programas
    path('programas/', formacion_views.listar_programas, name='programas'),
    path('programas/crear/', formacion_views.crear_programa, name='crear_programas'),

    # Competencias
    path('competencias/', formacion_views.listar_competencias, name='competencias'),
    path('competencias/crear/', formacion_views.crear_competencias,
         name='crear_competencias'),

    # Raps
    path('raps/', formacion_views.listar_raps, name='raps'),
    path('raps/crear/', formacion_views.crear_raps, name='crear_raps')


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
