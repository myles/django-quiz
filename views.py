from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from quiz.models import Quiz, Score
from quiz.forms import quiz_forms, QuestionForm

def quiz_dashboard(request):
	student = request.user
	quizzes = Quiz.objects.filter(students=student)
	scores = Score.objects.filter(student=student)
	
	return render_to_response('quiz/quiz_dashboard.html', { 'quizzes': quizzes, 'scores': scores }, context_instance=RequestContext(request))

def quiz_detail(request, slug):
	quiz = get_object_or_404(Quiz, slug__iexact=slug)
	form_list = quiz_forms(quiz)
	
	return render_to_response('quiz/quiz_detail.html', { 'form_list': form_list, 'quiz': quiz }, context_instance=RequestContext(request))
