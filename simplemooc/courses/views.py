from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import gettext_lazy as _

from .models import Course, Enrollment
from .forms import ContactCourse


# Create your views here.

def index(request):
    template_name = 'courses/courses.html'
    courses = Course.objects.all()
    context = {
        'courses': courses
    }
    return render(request, template_name, context)


def details(request, slug):
    course = get_object_or_404(Course, slug=slug)
    template_name = 'courses/details.html'
    context = {}
    if request.method == 'POST':
        form = ContactCourse(request.POST)
        if form.is_valid():
            context['is_valid'] = True
            form.send_mail(course)
            form = ContactCourse()  # volta o formulario com os dados vazios
    else:
        form = ContactCourse()
    context['form'] = form
    context['course'] = course
    return render(request, template_name, context)


@login_required
def enrollment(request, slug):
    course = get_object_or_404(Course, slug=slug)
    enrollments, created = Enrollment.objects.get_or_create(
        user=request.user, course=course)
    if created:
        messages.success(request, _('Você foi inscrito com sucesso no curso'))
        enrollments.active()
    else:
        messages.warning(request, _('Você já está inscrito no curso'))

    return redirect('accounts:dashboard')
