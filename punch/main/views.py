from django.views.generic import TemplateView, FormView
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect

from punch.main.forms import UserCreationForm
from punch.mixins import LoginRequiredMixin


class HomeView(TemplateView):
    template_name = 'home.html'


class AboutView(TemplateView):
    template_name = 'about.html'


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'


class RegisterView(CreateView):
    template_name = 'register.html'
    form_class = UserCreationForm
    success_url = '/dashboard'


class LoginView(FormView):
    template_name = 'login.html'
    form_class = AuthenticationForm
    success_url = '/dashboard'

    def form_valid(self, form):
        login(self.request, form.get_user())
        next_url = self.request.POST.get("next", self.success_url)
        return redirect(next_url)
