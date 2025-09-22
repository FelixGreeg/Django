from django.urls import path # type: ignore

from . import views

app_name = "polls"
urlpatterns = [
    path("", views.ListaEncuestas.as_view(), name="encuestas"),
    path("crear/", views.crear_pregunta, name="crear_pregunta"),
    path("crear/<int:pregunta_id>/opciones/", views.agregar_opcion, name="agregar_opcion"),
    path("<int:pk>/", views.DetalleEncuesta.as_view(), name="detalle"),
    path("<int:pk>/resultados/", views.ResultadosEncuesta.as_view(), name="resultados"),
    path("<int:pregunta_id>/votar/", views.votar, name="votar"),
    
]
