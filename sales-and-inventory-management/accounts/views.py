from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from .models import Profile
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm, UserUpdateForm, ProfileUpdateForm
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django_tables2 import SingleTableView
import django_tables2 as tables
from django_tables2.export.views import ExportMixin
from django_tables2.export.export import TableExport
from .tables import ProfileTable
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib import  messages
from django.core.mail import send_mail

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
    )

# Create your views here.
from django.views import View
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .forms import CreateUserForm


class RegisterView(CreateView):
    form_class = CreateUserForm
    template_name = "./accounts/register.html"
    model = User
    success_url = reverse_lazy("user-login")

    def form_valid(self, form):
        mail = form.cleaned_data.get("email")
        send_mail(
            "Thank You For Registration!!!!!",
            "Registration successfull!!!!",
            "inventorymanagement036@gmail.com",
            [mail]
        )
        messages.success(self.request, "Registration Completed !")
        self.object = form.save()
        return super().form_valid(form)



def profile(request):
    context = {

    }
    return render(request, 'accounts/profile.html', context)


def profile_update(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('user-profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'accounts/profile_update.html', context)

class ProfileListView(LoginRequiredMixin, ExportMixin, tables.SingleTableView):
    model = Profile
    template_name = 'accounts/stafflist.html'
    context_object_name = 'profiles'
    pagination = 10
    table_class = ProfileTable
    SingleTableView.table_pagination = False

class ProfileCreateView(LoginRequiredMixin, CreateView):
    model = Profile
    template_name = 'accounts/staffcreate'
    fields = ['user','role', 'status']

    def form_valid(self, form):
        return super().form_valid(form)

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        else:
            return False

    def get_success_url(self):
        return reverse('profile_list')

class ProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    template_name = 'accounts/staffupdate.html'
    fields = ['user','role', 'status']

    def form_valid(self, form):
        return super().form_valid(form)

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        else:
            return False
    def get_success_url(self):
        return reverse('profile_list')


class ProfileDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Profile
    template_name = 'accounts/staffdelete.html'

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        else:
            return False
    def get_success_url(self):
        return reverse('profile_list')