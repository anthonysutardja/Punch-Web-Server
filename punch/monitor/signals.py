from punch.monitor.lib.phone import send_sms


def check_and_send_alerts(reading):
    """Check and send all the alerts."""
    temperature = reading.temperature
    brix = reading.brix
    users = reading.tank.location.users.all()

    # Brix is greater than highest allowed level
    if reading.tank.alert_brix_high and brix >= reading.tank.alert_brix_high:
        message_to_users(
            users,
            BRIX_GREATER_TEMPLATE.format(
                tank_name=reading.tank.name,
                location_name=reading.tank.location.name,
                reading=brix,
                alert_level=reading.tank.alert_brix_high,
            )
        )

    # Brix is lower than lowest allowed level
    if reading.tank.alert_brix_low and brix <= reading.tank.alert_brix_low:
        message_to_users(
            users,
            BRIX_LESS_TEMPLATE.format(
                tank_name=reading.tank.name,
                location_name=reading.tank.location.name,
                reading=brix,
                alert_level=reading.tank.alert_brix_low,
            )
        )

    # Temp is greater than highest allowed level
    if reading.tank.alert_temp_high and temperature >= reading.tank.alert_temp_high:
        message_to_users(
            users,
            TEMP_GREATER_TEMPLATE.format(
                tank_name=reading.tank.name,
                location_name=reading.tank.location.name,
                reading=temperature,
                alert_level=reading.tank.alert_temp_high,
            )
        )

    # Temp is lower than lowest allowed level
    if reading.tank.alert_temp_low and temperature <= reading.tank.alert_temp_low:
        message_to_users(
            users,
            TEMP_LESS_TEMPLATE.format(
                tank_name=reading.tank.name,
                location_name=reading.tank.location.name,
                reading=temperature,
                alert_level=reading.tank.alert_temp_low,
            )
        )


def message_to_users(users, message):
    """Helper function to send a message to every user in the users list."""
    for user in users:
        send_sms(user.userprofile.phone_number, message)


BRIX_GREATER_TEMPLATE = "ALERT: Your tank {tank_name} at {location_name} is reading " \
                        "at {reading:.2f} degrees Brix, over the set limit of {alert_level:.2f}."

TEMP_GREATER_TEMPLATE = "ALERT: Your tank {tank_name} at {location_name} is reading " \
                        "at {reading:.2f} degrees Celcius, over the set limit of {alert_level:.2f}."

BRIX_LESS_TEMPLATE = "ALERT: Your tank {tank_name} at {location_name} is reading " \
                     "at {reading:.2f} degrees Brix, under the set limit of {alert_level:.2f}."

TEMP_LESS_TEMPLATE = "ALERT: Your tank {tank_name} at {location_name} is reading " \
                     "at {reading:.2f} degrees Celcius, under the set limit of {alert_level:.2f}."
