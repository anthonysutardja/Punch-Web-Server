from django.core.cache import get_cache


cache = get_cache('default')


class RawBridge(object):

    def __init__(self, bridge_uuid):
        self.bridge_uuid = bridge_uuid

    def add_available_sensor(self, sensor_uuid):
        sensors = self.get_available_sensors()
        if not sensors:
            sensors = set()
        sensors.add(sensor_uuid)
        cache.set(self._get_sensor_key(), sensors, timeout=None)

    def remove_available_sensor(self, sensor_uuid):
        sensors = self.get_available_sensors()
        if sensors and sensor_uuid in sensors:
            try:
                sensors.remove(sensor_uuid)
                cache.set(self._get_sensor_key(), sensors, timeout=None)
            except KeyError:
                pass

    def get_available_sensors(self):
        return cache.get(self._get_sensor_key())

    def _get_sensor_key(self):
        return 'bridge:{bid}:sensors'.format(bid=self.bridge_uuid)
