from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import Links
from .forms import LinksForm, UserForm, UserUpdateForm
from django.contrib.auth import login
from django.contrib.auth.models import User

# Create individual link from id
def idToShortURL(id):
    map = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    shortURL = ""
    while(int(id) > 0):
        shortURL += map[id % 62]
        id //= 62
    return shortURL[len(shortURL): : -1]

class LinksListView(LoginRequiredMixin, View):
    template_name = 'links/list.html'

    def get(self, request):
        context = {}
        str_search = request.GET.get("search", False)
        if str_search:
            queryset = Links.objects.filter(user=request.user.id, original__contains=str_search).order_by("-created_at")
        else:
            queryset = Links.objects.filter(user=request.user.id).order_by("-created_at")
        context['object_list'] = queryset
        return render(request, self.template_name, context)

    def post(self, request, id=None):
        queryset = Links.objects.filter(user=request.user.id)
        for obj in queryset:
            if request.POST.get("delete" + str(obj.id)):
                obj.delete()
                return redirect("/links/")

class LinksCreateView(View):
    template_name = 'links/create.html'

    def get(self, request):
        form = LinksForm()
        context = {}
        context['form'] = form
        return render(request, self.template_name, context)

    def post(self, request):
        form = LinksForm(request.POST or None)
        context = {}
        context['form'] = form
        if form.is_valid():
            form = form.save(commit=False)
            if request.user.is_authenticated:
                form.user = request.user
            form.save()
            form.slug = idToShortURL(form.id)
            form.save()
            obj = Links.objects.get(id=form.id)
            context['object'] = obj
        return render(request, self.template_name, context)

class SettingsView(LoginRequiredMixin, View):
    template_name = 'links/settings.html'
    def get(self, request):
        context = {}
        user = User.objects.get(id=request.user.id)
        update_user_form = UserUpdateForm(instance=user)
        context['update_user_form'] = update_user_form
        return render(request, self.template_name, context)

    def post(self, request):
        context = {}
        if request.POST.get('update_account'):
            user = User.objects.get(id=request.user.id)
            update_user_form = UserUpdateForm(request.POST, instance=user)
            if update_user_form.is_valid():
                user = update_user_form.save(commit=False)
                user.save()
                return redirect("/settings/")
            context['update_user_form'] = update_user_form
            return render(request, self.template_name, context)

# Redirect to original link + count clicks
class LinkRedirectView(View):
    def get(self, request, slug=None):
        try:
            obj = Links.objects.get(slug=slug, user=request.user.id)
            obj.counter += 1
            obj.save()
            return redirect(obj.original)
        except:
            return render(request, 'links/error.html')

class RegistrationView(View):
    template_name = 'registration/registration.html'

    def get(self, request):
        context = {}
        form = UserForm()
        context['form'] = form
        return render(request, self.template_name, context)

    def post(self, request):
        if request.POST.get('registration'):
            form = UserForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.username = user.username.lower()
                user.save()
                login(request, user)
                return redirect("/")
            return render(request, self.template_name, {'form': form})