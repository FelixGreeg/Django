from django.shortcuts import render # type: ignore

def mapa_view(request):
    return render(request, 'mapa/leaflet.html')
