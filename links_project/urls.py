from django.contrib import admin
from django.urls import include, path
from links.views import *

urlpatterns = [
    path("", LinksCreateView.as_view(), name="link_create"),
    path("links/", links_list_view, name="links"),
    path('admin/', admin.site.urls),
    path("registration/", registration_view, name="registration"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path('', include('django.contrib.auth.urls')),
    path("<slug:slug>/", link_redirect_view, name="link"),
]