from django import forms

from punch.monitor.models import Tank, Bridge


class TankCreationForm(forms.ModelForm):
    """
    A form for creating a new tank. This form ensures that no new tanks are added that have a sensor ID that is also
    active for another tank.
    """
    error_messages = {
        'duplicate_sensor': "An active tank has already registered this sensor.",
    }

    name = forms.CharField(label="Name", max_length=80)
    sensor_uuid = forms.CharField(label="Sensor UUID", max_length=32)
    alert_temp_high = forms.FloatField(label="Highest temperature that triggers alert", required=False)
    alert_temp_low = forms.FloatField(label="Low temperature that triggers alert", required=False)

    class Meta:
        model = Tank
        fields = ("sensor_uuid", "name", "alert_temp_high", "alert_temp_low")

    def clean_sensor_uuid(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        sensor_uuid = self.cleaned_data["sensor_uuid"]
        try:
            Tank.objects.get(sensor_uuid=sensor_uuid, ended_at=None)
        except Tank.DoesNotExist:
            return sensor_uuid
        raise forms.ValidationError(
            self.error_messages['duplicate_sensor'],
            code='duplicate_sensor_uuid',
        )


class BridgeCreationForm(forms.ModelForm):
    """
    A form for adding a new bridge.
    """
    uuid = forms.CharField(label="Bridge UUID", max_length=32)

    class Meta:
        model = Bridge
        fields = ('uuid',)

    def clean_uuid(self):
        """Clean the uuid for unnecessary hyphens."""
        return self.cleaned_data["uuid"].replace('-', '')
