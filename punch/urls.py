from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt

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
    url(r'^location/(?P<l_pk>\d+)/tank/add$', monitor_views.TankCreateView.as_view(), name='tank-create'),
    url(r'^location/(?P<l_pk>\d+)/tank/(?P<pk>\d+)/$', monitor_views.TankView.as_view(), name='tank-create'),
    url(r'^location/(?P<l_pk>\d+)/tank/(?P<pk>\d+)/end$', monitor_views.TankFinishRedirectView.as_view(), name='tank-finish'),
    # Update entry point
    url(r'^updater$', csrf_exempt(monitor_views.BridgeEntryView.as_view()), name='reading-entry-point'),
    url(r'^heartbeat$', csrf_exempt(monitor_views.HeartBeatEntryView.as_view()), name='heartbeat'),
    url(r'^admin/', include(admin.site.urls)),
)
