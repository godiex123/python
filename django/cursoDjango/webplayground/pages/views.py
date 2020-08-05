from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from .models import Page
from .forms import PageForm

# Create your views here.

# Este es un metodo para validar
class StaffRequireMixin(object):
    """
    Este mixin requerira que el usuario sea miembro del staff
    """
    # Este es otro metodo para validar mas corto
    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        # con el decorador ya no iria esta parte
        #if not request.user.is_staff:
        #    return redirect(reverse_lazy('admin:login'))
        return super(StaffRequireMixin, self).dispatch(request, *args, **kwargs)    


class PageListView(ListView):
    model = Page

class PageDetailView(DetailView):
    model = Page

@method_decorator(staff_member_required, name="dispatch")
class PageCreate(CreateView):
    model = Page
    form_class = PageForm
    success_url = reverse_lazy('pages:pages')

@method_decorator(staff_member_required, name="dispatch")
class PageUpdate(UpdateView):
    model = Page
    form_class = PageForm
    template_name_suffix = '_update_form'
    
    def get_success_url(self):
        return reverse_lazy('pages:update', args=[self.object.id]) + '?ok'

@method_decorator(staff_member_required, name="dispatch")
class PageDelete(DeleteView):
    model = Page
    success_url = reverse_lazy('pages:pages')