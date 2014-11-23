from django.contrib.auth.models import User
from django.test import TestCase

from punch.monitor.models import Location, Bridge, Tank


class LocationTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='derp', password='herp')
        self.location = None

    def tearDown(self):
        if self.location:
            self.location.delete()
        self.user.delete()

    def test_add_new_location(self):
        """Verify that we can add a new location."""
        self.location = Location(name='1455 Market St')
        self.location.save()
        self.location.users.add(self.user)
        self.location.save()

        # Check that the user is there
        self.assertEqual(1, len(self.location.users.all()))


class BridgeTestCase(TestCase):

    def setUp(self):
        self.location = Location.objects.create(name='1455 Market St')
        self.bridge = None

    def tearDown(self):
        if self.bridge:
            self.bridge.delete()
        self.location.delete()

    def test_add_new_bridge(self):
        """Verify that we can add a new bridge to a new location."""
        self.bridge = Bridge(uuid='a1a1a1', location=self.location)
        self.bridge.save()


class TankTestCase(TestCase):

    def setUp(self):
        self.location = Location.objects.create(name='1455 Market St')
        self.tank = None

    def tearDown(self):
        if self.tank:
            self.tank.delete()
        self.location.delete()

    def test_add_new_tank(self):
        """Verify that we can add a new tank to a location."""
        self.tank = Tank(sensor_uuid='111111', location=self.location)
        self.tank.save()

        # Verify attributes
        self.assertIsNotNone(self.tank.started_at)
        self.assertTrue(self.tank.is_active)

    def test_deactivate_tank(self):
        """Verify that we can deactivate the tank."""
        self.tank = Tank(sensor_uuid='111111', location=self.location)
        self.tank.save()

        self.tank.deactivate()
        self.assertFalse(self.tank.is_active)
        self.assertLess(
            self.tank.started_at.replace(tzinfo=None),
            self.tank.ended_at.replace(tzinfo=None)
        )
