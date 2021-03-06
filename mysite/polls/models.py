import datetime

from django.db import models
from django.utils import timezone
from django.contrib import admin

# Each model is a subclass of django.db.models.Model
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    # variable stores field name in machine-friendly format
    # can use an optional first positional argument to a Field to designate a human-readable name
    pub_date = models.DateTimeField('date published') 
    
    # python version of a toString() method
    def __str__(self):
        return self.question_text

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    )

    # custom method
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now 

class Choice(models.Model):
    # Relationship defined using ForeignKey
    # Each Choice is related to a single Question
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # CharField requires max_length
    choice_text = models.CharField(max_length=200)
    # default is optional argument
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
