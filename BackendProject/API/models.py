from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ("1", 'student'),
        ("2", 'teacher'),
        ("3", 'supervisor'),
    )
    user_type = models.CharField(choices=USER_TYPE_CHOICES,default="1",null=False , max_length=10)

    def __str__(self):
        return self.username


class Teacher(models.Model):
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

class Exam(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    # TO DO
    # supervisor info

class Answer(models.Model):
    Question = models.ForeignKey('Question', on_delete=models.CASCADE , blank=True)
    text = models.TextField()


class Question(models.Model):
    Exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    text = models.TextField()
    mark = models.FloatField()
    previous_question = models.ForeignKey("Question" , on_delete=models.CASCADE , null=True)
    question_answer = models.ForeignKey(Answer,on_delete=models.CASCADE)
    # TO DO
    # Question info


def update_user_type(sender , instance , created , **kwargs):
    if created:
        if instance.user_type == "1":
            student = Student(user=instance)
            student.save()
        elif instance.user_type == "2":
            teacher = Teacher(user=instance)
            teacher.save()
        else:
            supervisor = Supervisor(user=instance)
            supervisor.save()
post_save.connect(update_user_type,sender=User)


