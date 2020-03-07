from django.conf import settings
from django.db import models
from django.utils.translation import  ugettext_lazy as _

# Custom Manager do model Course
from django.urls import reverse


class CourseManager(models.Manager):
    def search(self, query):
        return self.get_queryset().filter(
            models.Q(name__icontains=query) |
            models.Q(description__icontains=query)
        )


# Model Course
class Course(models.Model):
    name = models.CharField(verbose_name=_('nome'), max_length=100)
    slug = models.SlugField(_('atalho'))
    description = models.TextField(verbose_name=_('descricao'), blank=True)
    about = models.TextField(verbose_name=_('sobre o curso'), blank=True)
    start_date = models.DateField(
        verbose_name=_('data inicio'), blank=True, null=True
    )
    image = models.ImageField(
        verbose_name=_('imagem'), upload_to='courses/images',
        null=True, blank=True
    )

    created_at = models.DateTimeField(verbose_name=_('criado em'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('atualizado em'), auto_now=True)

    objects = CourseManager()

    # Retorna o nome do objecto a ser utilizado
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('courses:details', args=[self.slug])

    class Meta:
        verbose_name = _('curso')
        verbose_name_plural = _('cursos')
        ordering = ['name']


class Enrollment(models.Model):
    STATUS_CHOICES = (
        (0, _('Pendente')),
        (1, _('Aprovado')),
        (2, _('Cancelado')),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('usuário'), related_name='enrollments',
                             on_delete=models.CASCADE)
    course = models.ForeignKey(Course, verbose_name=_('curso'), related_name='enrollments', on_delete=models.CASCADE)
    status = models.IntegerField(verbose_name=_('status'), choices=STATUS_CHOICES, default=0, blank=True)
    create_at = models.DateTimeField(verbose_name=_('criado em'), auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_('actualizado em'), auto_now=True)

    def active(self):
        self.status = 1
        self.save()

    def is_approved(self):
        return self.status == 1

    class Meta:
        verbose_name = _('inscrição')
        verbose_name_plural = _('inscrições')
        unique_together = (('user', 'course'),)

class Announcement(models.Model):
	course = models.ForeignKey(Course, verbose_name=_('anúncio'), 
		on_delete=models.CASCADE, related_name='announcements')
	title = models.CharField(verbose_name=_('título'), max_length=100)
	content = models.TextField(verbose_name=_('conteúdo'), blank=True)	


	created_at = models.DateTimeField(verbose_name=_('criado em'), auto_now_add=True)
	updated_at = models.DateTimeField(verbose_name=_('actualiza em'), auto_now=True)

	def __str__(self):
		return self.title

	class Meta:
		verbose_name=_('anúncio')
		verbose_name_plural = _('anúncios')
		ordering = ['-created_at']


class Comment(models.Model):
	announcement = models.ForeignKey(Announcement, verbose_name=_('coment'),
	 on_delete=models.CASCADE, related_name='comments')
	user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('user'), on_delete=models.CASCADE)
	comment = models.TextField('comentário')

	created_at = models.DateTimeField(verbose_name=_('criado em'), auto_now_add=True)
	updated_at = models.DateTimeField(verbose_name=_('actualiza em'), auto_now=True)

	def __str__(self):
		return self.user.username


	class Meta:
		verbose_name=_('comentário')
		verbose_name_plural =_('comentários')
		ordering = ['created_at']
		