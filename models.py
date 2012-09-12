from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import permalink
from django.contrib.auth.models import User
from django.template.defaultfilters import truncatewords_html
from django.contrib import admin
from quiz.managers import *

class Category(models.Model):
	"""Category model."""
	title		= models.CharField(_('title'), max_length=100)
	slug		= models.SlugField(_('slug'), unique=True)
	
	class Meta:
		verbose_name = _('category')
		verbose_name_plural = _('categories')
		db_table = 'quiz_categories'
		ordering = ('title',)
	
	def __unicode__(self):
		return u'%s' % self.title
	
	@permalink
	def get_absolute_url(self):
		return ('quiz_category_detail', None, {'slug': self.slug})

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
	
admin.site.register(Category, CategoryAdmin)


class Quiz(models.Model):
	STATUS_CHOICES = (
		(1, _('Draft')),
		(2, _('Public')),
		(3, _('Close')),
	)
	title			= models.CharField(_('title'), max_length=100)
	slug			= models.SlugField(_('slug'))
	author			= models.ForeignKey(User, related_name='author')
	description		= models.TextField(_('description'), blank=True, null=True)
	status			= models.IntegerField(_('status'), choices=STATUS_CHOICES, default=1)
	publish			= models.DateTimeField(_('publish'))
	categories		= models.ManyToManyField(Category, blank=True)
	students		= models.ManyToManyField(User, blank=True, null=True, related_name='students')
	created			= models.DateTimeField(_('created'), auto_now_add=True)
	modified		= models.DateTimeField(_('modified'), auto_now=True)
	
	class Meta:
		verbose_name		= _('quiz')
		verbose_name_plural	= _('quizzes')
		db_table			= 'quizzes'
		ordering			= ('-publish',)
	
	
	def __unicode__(self):
		return u"%s" % self.title
	
	@property
	def count_questions(self):
		return Question.objects.filter(quiz=self).count()
	
	@permalink
	def get_absolute_url(self):
		return ('quiz_detail', None, {
			'slug':	self.slug,
		})
	
	@permalink
	def get_process_quiz_url(self):
		return ('process_quiz', None, {
			'slug':	self.slug,
		})

class QuizAdmin(admin.ModelAdmin):
    prepopulate_fields = {'slug': ('title',)}
    radio_fields = {'status': True}

admin.site.register(Quiz, QuizAdmin)

class Answer(models.Model):
	answer	= models.TextField(_('answer'))
	weight	= models.IntegerField(_('weight'), default=1)
	
	class Meta:
		verbose_name		= _('answer')
		verbose_name_plural	= _('answers')
		db_table			= 'quiz_answers'
	
	class Admin:
		pass
	
	def __unicode__(self):
		return u"%s" % truncatewords_html(self.answer, 10)

class Question(models.Model):
	quiz			= models.ForeignKey(Quiz)
	question		= models.TextField(_('question'))
	answers			= models.ManyToManyField(Answer)
	correct_answer	= models.ForeignKey(Answer, related_name="correct")
	
	class Meta:
		verbose_name		= _('question')
		verbose_name_plural	= _('questions')
		db_table			= 'quiz_questions'
	
	class Admin:
		list_display	= ('title', 'quiz')
		list_filter		= ('quiz',)
		search_fields	= ('question',)
		
	@property
	def title(self):
		return u"%s" % truncatewords_html(self.question, 10)
	
	def __unicode__(self):
		return self.title

class Score(models.Model):
	student			= models.ForeignKey(User, related_name='student')
	quiz			= models.ForeignKey(Quiz)
	corrent_anwsers	= models.ManyToManyField(Question, blank=True, null=True)
	quiz_taken		= models.DateTimeField(_('quiz taken'), auto_now_add=True)
	
	class Meta:
		verbose_name		= ('student score')
		verbose_name_plural	= ('student scores')
		db_table			= 'quiz_scores'
		unique_together		= (("student", "quiz"),)
	
	class Admin:
		list_display	= ('quiz', 'student', 'corrent_anwser_count', 'total_quiestions',)
		list_filter		= ('quiz', 'student')
	
	@permalink
	def get_absolute_url(self):
		return ('quiz_detail', None, {
			'slug':	self.quiz.slug,
		})
	
	@property
	def corrent_anwser_count(self):
		return self.corrent_anwsers.count()
	
	@property
	def total_quiestions(self):
		return self.quiz.count_questions
	
	def __unicode__(self):
		return u"%s took the quiz %s" % (self.student, self.quiz)
