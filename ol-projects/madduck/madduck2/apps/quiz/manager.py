from django.db.models import Manager

class QuizManager(Manager):
  quiz.quiz_questions.all().order_by('number'),
  pass

class QuestionManager(Manager):
  quiz.quiz_questions.all().order_by('number'),
  pass

class AnswerManager(Manager):
  pass