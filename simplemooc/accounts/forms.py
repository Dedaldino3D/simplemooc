from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from simplemooc.accounts.models import PasswordReset
from simplemooc.accounts.utils import generate_hash_key
from simplemooc.core.mail import send_mail_template
from django.utils.translation import  gettext_lazy as _

User = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField(label=_('Usuário'))
    password = forms.CharField(label=_('Senha'), widget=forms.PasswordInput)


class PasswordResetForm(forms.Form):
    email = forms.EmailField(label=_('E-mail'))

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            return email
        return forms.ValidationError(
            _('Nenhum usuário encontrado com este email')
        )

    def save(self):
        template_name = 'accounts/password_reset_mail.html'
        user = User.objects.get(email=self.cleaned_data['email'])
        key = generate_hash_key(user.username)
        reset = PasswordReset(key=key, user=user)
        reset.save()
        context = {
            'reset': reset
        }
        subject = _('Criar nova senha para a sua conta do SimpleMooc')
        send_mail_template(subject, template_name,
                           context, [user.email]
                           )


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label=_('Senha'), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Confirmação de Senha'), widget=forms.PasswordInput)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                _('A confirmação de senha está incorreta')
            )
        return password2

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()

        return user

    class Meta:
        model = User
        fields = ['username', 'email']


class EditAccount(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'name', 'email']
