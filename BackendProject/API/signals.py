from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *

@receiver(post_save,sender=User)
def update_user_type(sender , instance , created , **kwargs):
    if created:
        if instance.user_type == "1":
            student = Student(user=instance)
            student.save()
        elif instance.user_type == "2":
            examiner = Examiner(user=instance)
            examiner.save()
        else:
            supervisor = Supervisor(user=instance)
            supervisor.save()
