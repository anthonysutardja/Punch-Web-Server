from django.conf.urls import patterns, include, url
from django.contrib import admin

from punch.main import views as main_views
from punch.monitor import views as monitor_views


urlpatterns = patterns(
    '',
    # My URLS here
    url(r'^$', main_views.HomeView.as_view()),
    url(r'^signup$', main_views.RegisterView.as_view()),
    url(r'^login$', main_views.LoginView.as_view()),
    url(r'^logout$', main_views.LogoutView.as_view()),
    url(r'^dashboard$', main_views.DashboardView.as_view()),
    # Monitoring URLs
    url(r'^location/create$', monitor_views.LocationCreateView.as_view()),
    url(r'^location/(?P<pk>\d+)/$', monitor_views.LocationView.as_view(), name='location-detail'),
    url(r'^location/(?P<pk>\d+)/edit$', monitor_views.LocationEditView.as_view(), name='location-edit'),
    url(r'^location/(?P<l_pk>\d+)/bridge/add$', monitor_views.BridgeCreateView.as_view(), name='bridge-create'),
    url(r'^admin/', include(admin.site.urls)),
)
