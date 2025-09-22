from django.urls import path # type: ignore

from . import views
app_name = "leaflet"
urlpatterns = [
    path('', views.mapa_view, name='mapa'),
]