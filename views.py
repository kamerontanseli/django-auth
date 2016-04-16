from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from crispy_forms.helper import FormHelper
from django.core.urlresolvers import reverse
from .forms import *

# Create your views here.

def login_user(request, username, password):
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return "allowed"
        else:
            return "disabled"
    else:
        return "incorrect"


def login_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    status = login_user(request, username, password)
    return JsonResponse({'status': status})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("user_login"))

class UserLoginView(TemplateView):
    model = User
    template_name = "auth/user_login.html"
    success_url = "/admin/"
    def get_context_data(self, **kwargs):
        if 'view' not in kwargs:
            kwargs['view'] = self
        kwargs['success_url'] = self.success_url
        return kwargs

class UserCreateView(CreateView):
    model =  User
    form_class = UserCreateForm
    template_name = "auth/user_create.html"
    success_url = "/admin/"
    def form_valid(self, form):
        self.object = User.objects.create_user(
            username=form.instance.username,
            password=form.instance.password,
            email=form.instance.email
        )
        user = authenticate(username=self.object.username, password=form.instance.password)
        status = login(self.request, user)
        return HttpResponseRedirect(self.success_url)
