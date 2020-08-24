from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass
    # completed = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="completed", blank=True, null=True)

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=64)
    desc = models.CharField(max_length=200)
    due = models.DateField()
    urgency = models.CharField(max_length=20)
    completed = models.ManyToManyField(User)
    def __str__(self):
        return self.title
