from django import forms

from punch.monitor.models import Tank


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

    class Meta:
        model = Tank
        fields = ("sensor_uuid", "name")

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
