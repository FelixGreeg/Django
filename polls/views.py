from django.db.models import F # type: ignore
from django.http import HttpResponseRedirect # type: ignore
from django.shortcuts import get_object_or_404, render, redirect # type: ignore
from django.urls import reverse # type: ignore
from django.views import generic # type: ignore
from .formulario import PreguntaFormulario, OpcionFormulario

from polls.models import Pregunta, Opcion


class ListaEncuestas(generic.ListView):
    template_name = "polls/encuesta.html"
    context_object_name = "lista_ultimas_preguntas"

    def get_queryset(self):
        """Regresa todas las preguntas ordenadas por fecha de publicación descendente."""
        return Pregunta.objects.order_by("-fecha_publicacion")

class DetalleEncuesta(generic.DetailView):
    model = Pregunta
    template_name = "polls/detail.html"

class ResultadosEncuesta(generic.DetailView):
    model = Pregunta
    template_name = "polls/results.html"

def votar(request, pregunta_id):
    pregunta = get_object_or_404(Pregunta, pk=pregunta_id)
    try:
        opcion_seleccionada = pregunta.opcion_set.get(pk=request.POST["opinion"])
    except (KeyError, Opcion.DoesNotExist):
        # Volver a mostrar el formulario de votación.
        return render(
            request,
            "polls/detail.html",
            {
                "pregunta": pregunta,
                "error_message": "No has seleccionado una opción.",
            },
        )
    else:
        opcion_seleccionada.votos = F("votos") + 1
        opcion_seleccionada.save()
        # Siempre regresar un HttpResponseRedirect después de procesar correctamente
        # los datos POST. Esto previene que los datos se envíen dos veces si el usuario
        # presiona el botón de regresar.
    return HttpResponseRedirect(reverse("polls:resultados", args=(pregunta.id,)))

def crear_pregunta(request):
    if request.method == "POST":
        formulario = PreguntaFormulario(request.POST)
        if formulario.is_valid():
            pregunta = formulario.save()
            return HttpResponseRedirect(reverse("polls:agregar_opcion", args=(pregunta.id,)))
    else:
        formulario = PreguntaFormulario()
    return render(request, "polls/crear_pregunta.html", {"formulario": formulario})

def agregar_opcion(request, pregunta_id):
    pregunta = get_object_or_404(Pregunta, pk=pregunta_id)
    if request.method == "POST":
        formulario = OpcionFormulario(request.POST)
        if formulario.is_valid():
            opcion = formulario.save(commit=False)
            opcion.pregunta = pregunta
            opcion.save()
            return redirect('polls:agregar_opcion', pregunta_id=pregunta.id) 
    else:
        formulario = OpcionFormulario()
    
    contexto = {
        'pregunta': pregunta,
        'formulario': formulario,
        'opciones': pregunta.opcion_set.all()
    }
    return render(request, 'polls/agregar_opcion.html', contexto)