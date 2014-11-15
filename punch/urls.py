from django.conf.urls import patterns, include, url
from django.contrib import admin

from punch.main.views import (
    HomeView,
    RegisterView,
    LoginView,
    DashboardView,
)


urlpatterns = patterns(
    '',
    # My URLS here
    url(r'^$', HomeView.as_view()),
    url(r'^signup$', RegisterView.as_view()),
    url(r'^login$', LoginView.as_view()),
    url(r'^dashboard$', DashboardView.as_view()),
    url(r'^admin/', include(admin.site.urls)),
)
