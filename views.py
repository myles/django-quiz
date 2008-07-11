from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from quiz.models import Quiz, Score
from quiz.forms import quiz_forms, QuestionForm

def quiz_dashboard(request):
	student = request.user
	quizzes = Quiz.objects.filter(students=student)
	scores = Score.objects.filter(student=student)
	
	return render_to_response('quiz/quiz_dashboard.html', { 'quizzes': quizzes, 'scores': scores }, context_instance=RequestContext(request))

def quiz_detail(request, slug):
	quiz = get_object_or_404(Quiz, slug__iexact=slug)
	try:
		score = quiz.score_set.get(student=request.user, quiz=quiz)
		questions = quiz.question_set.all()
		corrent_anwser = score.corrent_anwsers
		return render_to_response('quiz/quiz_score.html', { 'quiz': quiz, 'score': score, 'questions': questions, 'corrent_anwser': corrent_anwser })
	except Score.DoesNotExist:
		form_list = quiz_forms(quiz)
		return render_to_response('quiz/quiz_detail.html', { 'form_list': form_list, 'quiz': quiz }, context_instance=RequestContext(request))

def process_quiz(request, slug):
	quiz = get_object_or_404(Quiz, slug__iexact=slug)
	
	if request.method == 'POST':
		form_list = quiz_forms(quiz, request.POST)
		score = Score()
		score.student = request.user
		score.quiz = quiz
		score.save()
		
		for form in form_list:
			if form.is_correct():
				score.corrent_anwsers = form.question
				score.save()
		
		return HttpResponseRedirect(score.get_absolute_url())
	
	return HttpResponseRedirect(quiz.get_absolute_url())