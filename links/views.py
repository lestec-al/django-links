from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import Links
from .forms import LinksForm, UserForm
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login

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
        queryset = Links.objects.filter(user=request.user.id)
        context = {'object_list': queryset}
        return render(request, self.template_name, context)

    def post(self, request, id=None):
        try:
            queryset = Links.objects.filter(user=request.user.id)
            for obj in queryset:
                if request.POST.get(str(obj.id)):
                    obj.delete()
                    return redirect("/")
            context = {'object_list': queryset}
            return render(request, self.template_name, context)
        except:
            return render(request, 'links/error.html')

class LinksCreateView(LoginRequiredMixin, View):
    template_name = 'links/create.html'
    def get(self, request):
        form = LinksForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LinksForm(request.POST or None)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            form.slug = idToShortURL(form.id)
            form.save()
            return redirect("/%d/"%form.id)
        return render(request, self.template_name, {'form': form})

class LinkSlugView(View):
    def get(self, request, slug=None):
        try:
            obj = Links.objects.get(slug=slug, user=request.user.id)
            return redirect(obj.original)
        except:
            return render(request, 'links/error.html')

class LinkDetailView(LoginRequiredMixin, View):
    template_name = 'links/detail.html'

    def get(self, request, id=None):
        try:
            context = {}
            obj = Links.objects.get(id=id, user=request.user.id)
            context['object'] = obj
            return render(request, self.template_name, context)
        except:
            return render(request, 'links/error.html')

    def post(self, request, id=None):
        try:
            context = {}
            obj = Links.objects.get(id=id, user=request.user.id)
            if request.POST.get('delete'):
                obj.delete()
                return redirect("/")
            return render(request, self.template_name, context)
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
            context = {}
            g = Group.objects.get(name='Common Users')
            if request.POST.get('registration'):
                form = UserForm(request.POST)
                if form.is_valid():
                    form.save()
                    username = form.cleaned_data.get('username')
                    raw_password = form.cleaned_data.get('password1')
                    user = authenticate(username=username, password=raw_password)
                    login(request, user)
                    g.user_set.add(user.id)
                    return redirect("/")
                return render(request, self.template_name, {'form': form})