from django.shortcuts import redirect, get_object_or_404
from django.views.generic import DetailView, TemplateView, FormView, RedirectView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from punch.monitor.models import (
    Location,
    Bridge,
    Tank,
)
from punch.monitor.forms import TankCreationForm
from punch.mixins import LoginRequiredMixin


# TODO: permissions based on location ownership
# https://docs.djangoproject.com/en/1.7/topics/class-based-views/mixins/

# Good reference forms in general:
# https://docs.djangoproject.com/en/1.7/topics/class-based-views/generic-display/
# https://docs.djangoproject.com/en/1.7/topics/class-based-views/generic-editing/


class LocationCreateView(LoginRequiredMixin, CreateView):
    model = Location
    fields = ('name', 'users')


class LocationEditView(LoginRequiredMixin, UpdateView):
    model = Location


class LocationDeleteView(LoginRequiredMixin, DeleteView):
    model = Location


class LocationView(LoginRequiredMixin, DetailView):
    model = Location

    def get_context_data(self, **kwargs):
        context = super(LocationView, self).get_context_data(**kwargs)
        context['active_tanks'] = [tank for tank in self.object.tank_set.all() if tank.is_active]
        context['finished_tanks'] = [tank for tank in self.object.tank_set.all() if not tank.is_active]
        return context

    def dispatch(self, request, *args, **kwargs):
        location = get_object_or_404(Location, pk=kwargs['pk'])
        if location and not location.bridge_set.all():
            return redirect(location.get_absolute_url() + 'bridge/add')
        return super(LocationView, self).dispatch(request, *args, **kwargs)


class BridgeCreateView(LoginRequiredMixin, CreateView):
    model = Bridge
    fields = ('uuid', )

    def get_context_data(self, **kwargs):
        context = super(BridgeCreateView, self).get_context_data(**kwargs)
        location = Location.objects.get(pk=int(self.kwargs.get('l_pk')))
        context['location'] = location
        context['needs_bridge'] = 1 - len(location.bridge_set.all())
        return context

    def form_valid(self, form):
        location = Location.objects.get(pk=self.kwargs.get('l_pk'))
        form.instance.location = location
        return super(BridgeCreateView, self).form_valid(form)


class BridgeDeleteView(LoginRequiredMixin, DeleteView):
    model = Bridge


class TankCreateView(LoginRequiredMixin, CreateView):
    model = Tank
    form_class = TankCreationForm
    fields = ('sensor_uuid', 'name')

    def get_context_data(self, **kwargs):
        context = super(TankCreateView, self).get_context_data(**kwargs)
        location = Location.objects.get(pk=int(self.kwargs.get('l_pk')))
        context['location'] = location
        return context

    def form_valid(self, form):
        location = Location.objects.get(pk=self.kwargs.get('l_pk'))
        form.instance.location = location
        return super(TankCreateView, self).form_valid(form)


class TankEditView(LoginRequiredMixin, UpdateView):
    model = Tank


class TankDeleteView(LoginRequiredMixin, DeleteView):
    model = Tank


class TankView(LoginRequiredMixin, DetailView):
    model = Tank

    def get_context_data(self, **kwargs):
        context = super(TankView, self).get_context_data(**kwargs)
        location = Location.objects.get(pk=int(self.kwargs.get('l_pk')))
        context['location'] = location
        return context


class TankFinishRedirectView(RedirectView):

    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        tank = get_object_or_404(Tank, pk=kwargs['pk'])
        tank.deactivate()
        tank.save()
        return tank.get_absolute_url()
