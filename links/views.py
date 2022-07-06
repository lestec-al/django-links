from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import Link
from .forms import *
from django.contrib.auth import login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required

@login_required
def links_list_view(request):
    context = {}
    str_search = request.GET.get("search", False)
    if str_search:
        queryset = Link.objects.filter(user=request.user.id, original__contains=str_search).order_by("-created_at")
    else:
        queryset = Link.objects.filter(user=request.user.id).order_by("-created_at")
    context["object_list"] = queryset

    if request.method == "POST":
        id = int(list(request.POST.keys())[-1][list(request.POST.keys())[-1].index('-'):][1:])
        obj = Link.objects.get(id=id)
        if request.POST.get(f"delete-{str(id)}"):
            obj.delete()
            return redirect("/links/")
        if request.POST.get(f"edit-{str(id)}"):
            context["edit_form"] = EditSlugForm()
            context["edit_obj"] = obj
        if request.POST.get(f"save_edit_link-{str(id)}"):
            form = EditSlugForm(request.POST)
            context["edit_form"] = form
            context["edit_obj"] = obj
            # Slug validation
            forbidden = ["links","admin","registration","profile","login","logout","password_change","password_reset","reset"]
            if (form.is_valid() and
                len([f for f in forbidden if f in form.cleaned_data.get("slug")]) == 0 and
                len([o for o in Link.objects.filter(slug=form.cleaned_data.get("slug")) if o != obj]) == 0
                ):
                obj.slug = form.cleaned_data.get("slug")
                obj.save()
                return redirect("/links/")
            else:
                context["not_valid"] = True
    return render(request, "links/list.html", context)

class LinksCreateView(View):
    template_name = "links/create.html"
    def get(self, request):
        form = LinksForm()
        context = {}
        context["form"] = form
        return render(request, self.template_name, context)

    def post(self, request):
        form = LinksForm(request.POST or None)
        context = {}
        context["form"] = form
        if form.is_valid():
            form = form.save(commit=False)
            if request.user.is_authenticated:
                form.user = request.user
            form.save()
            obj = Link.objects.get(id=form.id)
            context["object"] = obj
        return render(request, self.template_name, context)

class ProfileView(LoginRequiredMixin, View):
    template_name = "links/profile.html"
    def get(self, request):
        context = {}
        context["update_user_form"] = UserUpdateForm(instance=request.user)
        context["update_password_form"] = PasswordChangeForm(user=request.user)
        return render(request, self.template_name, context)

    def post(self, request):
        context = {}
        if request.POST.get("update_password"):
            update_password_form = PasswordChangeForm(data=request.POST, user=request.user)
            if update_password_form.is_valid():
                update_password_form.save()
                return redirect("/profile/")
            context["update_password_form"] = update_password_form
        if request.POST.get("update_account"):
            update_user_form = UserUpdateForm(data=request.POST, instance=request.user)
            if update_user_form.is_valid():
                update_user_form.save()
                return redirect("/profile/")
            context["update_user_form"] = update_user_form
        return render(request, self.template_name, context)

def link_redirect_view(request, slug=None):
    """Redirect to original link + count clicks"""
    try:
        obj = Link.objects.get(slug=slug)
        obj.counter += 1
        obj.save()
        return redirect(obj.original)
    except:
        return render(request, "links/error.html")  

def registration_view(request):
    context = {}
    form = UserForm(request.POST or None)
    context["form"] = form
    if request.POST.get("registration"):
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("/")
    return render(request, "registration/registration.html", context)