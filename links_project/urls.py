from django.contrib import admin
from django.urls import include, path
from links.views import LinksListView, LinksCreateView, RegistrationView, LinkRedirectView

urlpatterns = [
    path("", LinksCreateView.as_view(), name="link_create"),
    path("links/", LinksListView.as_view(), name="links"),
    path('admin/', admin.site.urls),
    path("registration/", RegistrationView.as_view(), name="registration"),
    path('accounts/', include('django.contrib.auth.urls')),
    path("<slug:slug>/", LinkRedirectView.as_view(), name="link"),
]