from django import forms
from django.conf import settings
from simplemooc.core.mail import send_mail_template
from django.utils.translation import gettext_lazy as _


class ContactCourse(forms.Form):
    name = forms.CharField(label=_('Nome'), max_length=100)
    email = forms.EmailField(label=_('Email'))
    message = forms.CharField(
        label=_('Mensagem'), widget=forms.Textarea
    )

    def send_mail(self, course):
        subject = _('[%s] Contato' % course)
        context = {
            'name': self.cleaned_data['name'],
            'email': self.cleaned_data['email'],
            'message': self.cleaned_data['message']
        }

        template_name = 'courses/contact_mail.html'

        send_mail_template(subject,
                           template_name, context,
                           [settings.CONTACT_EMAIL]
                           )
