import os

from twilio.rest import TwilioRestClient


# Our twilio phone number
TWILIO_PHONE_NUMBER = '+14155992671'


# Grab environment variables for credentials
ACCOUNT_SID = os.environ.get('TWILIO_API_SID', '')
AUTH_TOKEN = os.environ.get('TWILIO_API_TOKEN', '')


# Setup the Twilio Rest Client
client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)


def send_sms(phone_number, msg):
    """Send an SMS message to the given phone number."""
    return client.messages.create(
        body=msg,
        to=phone_number,
        from_=TWILIO_PHONE_NUMBER,
    )


# TODO: Add phone call message in the future
