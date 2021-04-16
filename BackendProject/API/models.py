from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import SET_NULL

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ("1", 'student'),
        ("2", 'examiner'),
        ("3", 'supervisor'),
    )
    user_type = models.CharField(choices=USER_TYPE_CHOICES,default="1",null=False , max_length=10)

    def __str__(self):
        return self.username


class Examiner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # TO DO
    # teacher info

    def __str__(self):
        return self.user.username


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # TO DO
    # student info

    def __str__(self):
        return self.user.username


class Supervisor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # TO DO
    # supervisor info

    def __str__(self):
        return self.user.username

class Answer(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE,default=None, related_name='answer')
    text = models.TextField()
    is_correct = models.BooleanField(default=True)
    def __str__(self) -> str:
        qans = str(self.question)+  str(self.text)
        return str(qans)
class Exam(models.Model):
    examiner = models.ForeignKey(Examiner,default=None, on_delete=models.CASCADE)
    # TO DO
    # Exam info
    exam_name = models.CharField(max_length=255, default='None')
    exam_startdate = models.DateTimeField(null=True)
    exam_duration = models.FloatField(null=True)
   # attendance = models.ManyToManyField(Student, related_name='attendance') 
   # students = models.ManyToManyField(Student, related_name='allowed_students')
    def __str__(self) -> str:
        return str(self.exam_name)

class Question(models.Model):
    exam = models.ForeignKey(Exam, default=None, on_delete=models.CASCADE)
    text = models.TextField()
    mark = models.FloatField(null = True)
    previous_question = models.ForeignKey("Question" , on_delete=models.CASCADE , null=True , blank=True)
    # question_answer = models.ForeignKey(Answer,on_delete=models.CASCADE, null= True)
    # TO DO
    # Question info



    def __str__(self) -> str:
        return str(self.text)









