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


@login_required
def undo_enrollment(request, slug):
    course = get_object_or_404(Course, slug=slug)
    enrollment = get_object_or_404( Enrollment, user=request.user, course=course )

    if request.method == 'POST':
        enrollment.delete()
        messages.warning(request ,_('Você cancelou a sua inscrição no curso.'))
        return redirect("accounts:dashboard")
        
    context = {
        'course': course,
        'enrollment': enrollment
    }
    template = 'courses/undo_enrollment.html'
    # return redirect('accounts:dashboard')
    return render(request, template, context)



@login_required
def announcements(request, slug):
    course = get_object_or_404(Course, slug=slug)
    enrollment = get_object_or_404(
        Enrollment, user=request.user, course=course
    )
    if not request.user.is_staff:
        if not enrollment.is_approved():
            messages.error(request, _("A sua inscrição está pendente"))
            return redirect('accounts:dashboard')
    template = 'courses/announcement.html'
    context = {
        'course': course,
        'announcements': course.announcements.all()
    }
    return render(request, template, context)
