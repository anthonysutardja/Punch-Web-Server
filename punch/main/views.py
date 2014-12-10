from django.views.generic import TemplateView, FormView, RedirectView
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect

from punch.main.forms import UserCreationForm
from punch.mixins import LoginRequiredMixin


class HomeView(TemplateView):
    template_name = 'home.html'


class AboutView(TemplateView):
    template_name = 'about.html'


class DashboardView(LoginRequiredMixin, RedirectView):
    template_name = 'dashboard.html'

    def get_redirect_url(self, *args, **kwargs):
        locations = self.request.user.location_set.all()
        if locations:
            return locations[0].get_absolute_url()
        else:
            return '/location/create'


class RegisterView(CreateView):
    template_name = 'register.html'
    form_class = UserCreationForm
    success_url = '/dashboard'

    def form_valid(self, form):
        result = super(RegisterView, self).form_valid(form)

        # Login the user automatically after user is created
        user = authenticate(
            username=self.request.POST.get('username'),
            password=self.request.POST.get('password1')
        )
        login(self.request, user)

        return result


class LoginView(FormView):
    template_name = 'login.html'
    form_class = AuthenticationForm
    success_url = '/dashboard'

    def form_valid(self, form):
        login(self.request, form.get_user())
        next_url = self.request.POST.get("next", self.success_url)
        return redirect(next_url)


class LogoutView(RedirectView):
    url = '/login'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)