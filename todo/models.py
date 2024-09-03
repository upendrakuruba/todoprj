from django.db import models
from todoapp.models import User
# Create your models here

class Todo(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    todo_name = models.CharField( max_length=50)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.todo_name
    