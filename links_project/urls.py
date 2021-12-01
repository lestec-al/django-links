from django.contrib import admin
from django.urls import include, path
from links.views import LinksListView, LinksCreateView, RegistrationView, LinkRedirectView, SettingsView

urlpatterns = [
    path("", LinksCreateView.as_view(), name="link_create"),
    path("links/", LinksListView.as_view(), name="links"),
    path('admin/', admin.site.urls),
    path("registration/", RegistrationView.as_view(), name="registration"),
    path("settings/", SettingsView.as_view(), name="settings"),
    path('accounts/', include('django.contrib.auth.urls')),
    path("<slug:slug>/", LinkRedirectView.as_view(), name="link"),
]