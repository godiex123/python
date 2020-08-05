from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import PersonaFormulario
from .models import Persona
from django.views.generic import CreateView, UpdateView, DeleteView, ListView

# Create your views here.
# por funcion

#def index(request):
#    if request.method == "POST":
#        form = PersonaFormulario(request.POST)
#        if form.is_valid():
#            form.save()
#            return redirect("home")
#    else:
#        form = PersonaFormulario()
#        personas = Persona.objects.all()
#    return render(request, 'core/core.html', {'form':form, 'personas': personas})


# por clase

class index(CreateView):
    form_class = PersonaFormulario
    template_name = 'core/core.html'
    success_url = reverse_lazy("home")

    #def get_context_data(self, **kwargs):
    #    context = super(index, self).get_context_data(**kwargs)
    #    context['personas'] = Persona.objects.all()
    #    return context

class listarPersonas(ListView):
    model = Persona
    template_name = 'core/listar_personas.html'

class ModificarPersona(UpdateView):
    model = Persona
    form_class = PersonaFormulario
    template_name = 'core/modificar.html'
    success_url = reverse_lazy("listar")

class EliminarPersona(DeleteView):
    model = Persona
    template_name = 'core/eliminar.html'
    success_url = reverse_lazy("listar")









