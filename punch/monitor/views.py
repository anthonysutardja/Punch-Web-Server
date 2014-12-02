import json
from datetime import datetime, timedelta
from random import random

from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import DetailView, RedirectView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from punch.monitor.lib.raw_bridge import RawBridge
from punch.monitor.models import (
    Location,
    Bridge,
    Tank,
    Reading,
)
from punch.monitor.forms import TankCreationForm, BridgeCreationForm
from punch.monitor.signals import check_and_send_alerts
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
    form_class = BridgeCreationForm

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
        context['sensor_uuids'] = self.get_sensor_uuids(location)
        return context

    def form_valid(self, form):
        location = Location.objects.get(pk=self.kwargs.get('l_pk'))
        form.instance.location = location
        self.remove_sensor_uuid(location, form.instance.sensor_uuid)
        return super(TankCreateView, self).form_valid(form)

    def get_sensor_uuids(self, location):
        sensor_uuids = []
        for bridge in location.bridge_set.all():
            b = RawBridge(bridge.uuid)
            sensor_uuids.extend(list(b.get_available_sensors()))
        return sensor_uuids

    def remove_sensor_uuid(self, location, sensor_uuid):
        for bridge in location.bridge_set.all():
            b = RawBridge(bridge.uuid)
            b.remove_available_sensor(sensor_uuid)


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

        # Remove for now .. until we have real data
        # context['readings'] = serializers.serialize('json', self.object.reading_set.all())

        # Stub data below
        context['readings'] = serializers.serialize('json', self.create_fake_readings())
        return context

    # TODO: remove when we have real readings
    def create_fake_readings(self):
        readings = []
        for i in range(0, 100):
            t = random() * 10 + 20
            b = random() * 5 + 10
            d = datetime(2014, 11, 24, 18, 12, 8, 393455) + timedelta(minutes=15 * i)
            readings.append(Reading(temperature=t, brix=b, created_at=d))
        return readings


class TankFinishRedirectView(RedirectView):

    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        tank = get_object_or_404(Tank, pk=kwargs['pk'])
        tank.deactivate()
        tank.save()
        return tank.get_absolute_url()


class BridgeEntryView(View):

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            self.process_load(data)
        except ValueError:
            pass
        return HttpResponse(
            json.dumps({'received': True}),
            content_type='application/json',
            **kwargs
        )

    def process_load(self, data):
        bridge_uuid = str(data['bridge_uuid'].replace('-', ''))
        sensor_uuid = str(data['sensor_uuid'])
        temperature = float(data['temperature'])
        brix = float(data['brix'])
        try:
            tank = Tank.objects.get(sensor_uuid=sensor_uuid, ended_at=None)
            # If tank exists, add a new reading
            reading = Reading(temperature=temperature, brix=brix, tank=tank)
            # TODO: add signal for reading
            reading.save()
            check_and_send_alerts(reading)
        except Tank.DoesNotExist:
            # Otherwise, tank doesn't exist and should be noticed by the set.
            r_bridge = RawBridge(bridge_uuid)
            r_bridge.add_available_sensor(sensor_uuid)
