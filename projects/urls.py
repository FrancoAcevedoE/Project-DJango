from django.urls import path

from . import views

urlpatterns = [
    path("users/", views.home_index, name="home_index"),
    path("projects/<thematic>/", views.project_index, name="project_index"),
    path("project/<int:pk>/", views.project_detail, name="project_detail"),
    path("", views.home, name="project_home"),
    path("ponencias/", views.ponencias, name="ponencias"),
    path("ponencias/eje-<int:eje>/", views.ponencias_mesas, name="ponencias_mesas"),
    path("ponencias/eje-<int:eje>/?$", views.ponencias_mesas, name="ponencias_mesas"),
    path("ponencias/eje-<int:eje>/<int:pk>/", views.ponencias_individual, name="ponencias_individual"),
    path("ponencias/eje-<int:eje>/mesa-<int:mesa>/", views.ponencias_carrousel, name="ponencias_carrousel"),
    path("ponencias/eje-<int:eje>/mesa-<int:mesa>/<int:pk>/", views.ponencias_individual, name="ponencias_individual"),
    path("experiencias/", views.experiencias, name="experiencias"),
    path("experiencias/eje-<int:eje>/", views.experiencias_mesas, name="experiencias_mesas"),
    path("experiencias/eje-<int:eje>/?$", views.experiencias_mesas, name="experiencias_mesas"),
    path("experiencias/eje-<int:eje>/<int:pk>/", views.experiencias_individual, name="experiencias_individual"),
    path("experiencias/eje-<int:eje>/mesa-<int:mesa>/", views.experiencias_carrousel, name="experiencias_carrousel"),
    path("experiencias/eje-<int:eje>/mesa-<int:mesa>/<int:pk>/", views.experiencias_individual, name="experiencias_individual"),
    path("talleres/", views.talleres, name="talleres"),
    path("auditorio/", views.auditorio_mesas, name="auditorio_mesas"),
    path("auditorio/mesa-<int:mesa>/", views.auditorio_videos, name="auditorio_videos"),
]
