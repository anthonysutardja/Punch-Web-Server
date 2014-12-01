from datetime import datetime

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db import models


class Location(models.Model):
    """Model for describing a location which contains a bunch of sensors."""
    name = models.CharField(max_length=80)

    # For more details about many-to-many relationships in Django:
    # https://docs.djangoproject.com/en/dev/topics/db/examples/many_to_many/
    users = models.ManyToManyField(User)

    def get_absolute_url(self):
        return '/location/{id}/'.format(id=self.id)

    def __repr__(self):
        return '<Location: {name}>'.format(name=self.name)

    def __str__(self):
        return '<{name}>'.format(name=self.name)


class Bridge(models.Model):
    """Model that identifies a central hub."""
    # TODO: Figure out what this length should be
    uuid = models.CharField(max_length=32, unique=True)

    # For more details about many-to-one relationships in Django:
    # https://docs.djangoproject.com/en/1.7/topics/db/examples/many_to_one/
    location = models.ForeignKey(Location)

    def get_absolute_url(self):
        return self.location.get_absolute_url()


class Tank(models.Model):
    """Model that contains the fermentation tank abstraction."""
    # TODO: Figure out if this is the correct length for 128-bit hex identifier
    sensor_uuid = models.CharField(max_length=32)
    name = models.CharField(max_length=80)

    # Start/End date stuff
    # Automatically add the start date when the object is first created
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(blank=True, null=True)

    # For UI Placement
    y = models.IntegerField(blank=True, null=True)
    x = models.IntegerField(blank=True, null=True)

    # Relationships
    location = models.ForeignKey(Location)

    # Alert settings
    alert_temp_high = models.FloatField(blank=True, null=True)
    alert_temp_low = models.FloatField(blank=True, null=True)
    alert_brix_high = models.FloatField(blank=True, null=True)
    alert_brix_low = models.FloatField(blank=True, null=True)

    @property
    def is_active(self):
        """Return a boolean indicating if the tank is currently active."""
        return self.ended_at is None

    def deactivate(self):
        """Deactivate this tank."""
        if self.is_active:
            self.ended_at = datetime.utcnow()

    @property
    def total_days(self):
        """Return the number of days that the tank was active for."""
        return 0

    def get_absolute_url(self):
        return self.location.get_absolute_url() + 'tank/{id}/'.format(id=self.id)


class Reading(models.Model):
    """Model that contains each readings for a particular tank."""
    # Relationships
    tank = models.ForeignKey(Tank)

    # Metrics
    temperature = models.FloatField()
    brix = models.FloatField()

    # Time of reading
    created_at = models.DateTimeField(auto_now_add=True)
