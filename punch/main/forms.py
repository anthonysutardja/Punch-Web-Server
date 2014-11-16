from django import forms
from django.contrib.auth.models import User
from django.core.validators import EmailValidator

from punch.main.models import UserProfile


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

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        # The email and the username should be the same
        user.email = user.username


        # Force the save, disregard the commit flag
        user.save()

        # Hook it up to a user profile
        user_profile = UserProfile(user=user, phone_number=self.cleaned_data["phone_number"])
        user_profile.save()
        return user