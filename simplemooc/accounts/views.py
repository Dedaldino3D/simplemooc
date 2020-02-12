from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, SetPasswordForm
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _
from simplemooc.accounts.forms import LoginForm, RegisterForm, EditAccount, PasswordResetForm

# Create your views here.
from simplemooc.accounts.models import PasswordReset
from simplemooc.accounts.utils import generate_hash_key
from simplemooc.courses.models import Enrollment

User = get_user_model()

# My view for login
"""
def user_login(request):
    template_name = 'accounts/login.html'

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(settings.LOGIN_REDIRECT_URL)
                else:
                    return HttpResponse('Conta desativada')
            else:
                return redirect('')
    else:
        form = LoginForm()

    return render(request, template_name, {'form': form})
"""


def auth_login(request):
    template_name = 'registration/login.html'
    context = {}

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('core:home')
                else:
                    pass
        else:
            pass
    else:
        form = LoginForm()

    context['form'] = form
    return render(request, template_name, context)


def register(request):
    template_name = 'accounts/register.html'

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(request,
                                username=user.username,
                                password=form.cleaned_data['password1']
                                )
            login(request, user)
            return redirect('core:home')
        else:
            pass
    else:
        form = RegisterForm()
    context = {
        'form': form
    }
    return render(request, template_name, context)


@login_required
def dashboard(request):
    template_name = 'accounts/dashboard.html'
    context = {}
    context['enrollments'] = Enrollment.objects.filter(user=request.user)
    return render(request, template_name, context)


@login_required
def edit(request):
    template_name = 'accounts/edit.html'
    context = {}
    if request.method == "POST":
        form = EditAccount(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _('Os dados da sua conta foram alterados com sucesso'))
            return redirect('accounts:dashboard')
    else:
        form = EditAccount(instance=request.user)
    context['form'] = form
    return render(request, template_name, context)


@login_required
def edit_password(request):
    template_name = 'accounts/editPassword.html'
    context = {}
    if request.method == "POST":
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _('A sua senha foi alterada com sucesso'))
    else:
        form = PasswordChangeForm(user=request.user)
    context['form'] = form
    return render(request, template_name, context)


def passwordReset(request):
    template_name = 'accounts/password_reset.html'
    context = {}
    form = PasswordResetForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data['email']
        form.save()
        context['email'] = email
        context['success'] = True

    context['form'] = form
    return render(request, template_name, context)


def password_reset_confirm(request, key):
    template_name = 'accounts/password_reset_confirm.html'
    context = {}
    reset = get_object_or_404(PasswordReset, key=key)
    form = SetPasswordForm(user=reset.user, data=request.POST or None)
    if form.is_valid():
        form.save()
        context['success'] = True

    context['form'] = form

    return render(request, template_name, context)
