from django.test import TestCase


class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'duplicate_username': "A user with that username already exists.",
        'password_mismatch': "The two password fields didn't match.",
    }

    username = forms.CharField(label="Email address", max_length=30, validators=[EmailValidator])

    password1 = forms.CharField(label="Password",
        widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm password",
        widget=forms.PasswordInput,
        help_text="Enter the same password as above, for verification.")

    phone_number = forms.CharField(label="Phone number", max_length=17, validators=[UserProfile.phone_regex])

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name")