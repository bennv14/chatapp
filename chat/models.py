from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime
# Create your models here.

class Chat(models.Model):
    name = models.TextField(max_length=50)
    members = models.ManyToManyField(User)
    date_creat = models.DateField(default=date.today)
    User.objects.filter()
    
    def __str__(self) -> str:
        return self.name
    
    
class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(max_length=255)
    time_send = models.DateTimeField(default=datetime.now)
    def __str__(self) -> str:
        return self.message