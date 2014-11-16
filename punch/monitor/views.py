from django.views.generic import DetailView, TemplateView, FormView, RedirectView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from punch.monitor.models import (
    Location,
    Bridge,
    Tank,
)
from punch.mixins import LoginRequiredMixin


# TODO: permissions based on location ownership
# https://docs.djangoproject.com/en/1.7/topics/class-based-views/mixins/

# Good reference forms in general:
# https://docs.djangoproject.com/en/1.7/topics/class-based-views/generic-display/
# https://docs.djangoproject.com/en/1.7/topics/class-based-views/generic-editing/


class LocationCreateView(LoginRequiredMixin, CreateView):
    model = Location


class LocationEditView(LoginRequiredMixin, UpdateView):
    model = Location


class LocationDeleteView(LoginRequiredMixin, DeleteView):
    model = Location


class LocationView(LoginRequiredMixin, DetailView):
    model = Location


class BridgeCreateView(LoginRequiredMixin, CreateView):
    model = Bridge
    fields = ('uuid', )

    def get_context_data(self, **kwargs):
        context = super(BridgeCreateView, self).get_context_data(**kwargs)
        location = Location.objects.get(pk=int(self.kwargs.get('l_pk')))
        context['location'] = location
        return context

    def form_valid(self, form):
        location = Location.objects.get(pk=self.kwargs.get('l_pk'))
        form.instance.location = location
        return super(BridgeCreateView, self).form_valid(form)


class BridgeDeleteView(LoginRequiredMixin, DeleteView):
    model = Bridge


class TankCreateView(LoginRequiredMixin, CreateView):
    model = Tank


class TankEditView(LoginRequiredMixin, UpdateView):
    model = Tank


class TankDeleteView(LoginRequiredMixin, DeleteView):
    model = Tank


class TankView(LoginRequiredMixin, DetailView):
    model = Tank
