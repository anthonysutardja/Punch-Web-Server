from datetime import datetime

from django.contrib.auth.models import User
from django.db import models


class Location(models.Model):
    """Model for describing a location which contains a bunch of sensors."""
    name = models.CharField(max_length=80)

    # For more details about many-to-many relationships in Django:
    # https://docs.djangoproject.com/en/dev/topics/db/examples/many_to_many/
    users = models.ManyToManyField(User)


class Bridge(models.Model):
    """Model that identifies a central hub."""
    # TODO: Figure out what this length should be
    uuid = models.CharField(max_length=32, unique=True)

    # For more details about many-to-one relationships in Django:
    # https://docs.djangoproject.com/en/1.7/topics/db/examples/many_to_one/
    location = models.ForeignKey(Location)


class Tank(models.Model):
    """Model that contains the fermentation tank abstraction."""
    # TODO: Figure out if this is the correct length for 128-bit hex identifier
    sensor_uuid = models.CharField(max_length=32)

    # Start/End date stuff
    # Automatically add the start date when the object is first created
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(blank=True, null=True)

    # Relationships
    location = models.ForeignKey(Location)

    @property
    def is_active(self):
        """Return a boolean indicating if the tank is currently active."""
        return self.ended_at is None

    def deactivate(self):
        """Deactivate this tank."""
        if self.is_active:
            self.ended_at = datetime.utcnow()