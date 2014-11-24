from django.core.cache import get_cache


cache = get_cache('default')


class RawBridge(object):

    def __init__(self, bridge_uuid):
        self.bridge_uuid = bridge_uuid

    def set_available_sensors(self, sensor_uuid_list):
        return cache.set(self._get_sensor_key(), sensor_uuid_list, timeout=None)

    def get_available_sensors(self):
        return cache.get(self._get_sensor_key())

    def _get_sensor_key(self):
        return 'bridge:{bid}:sensors'.format(bid=self.bridge_uuid)
