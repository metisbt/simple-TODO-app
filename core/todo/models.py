from django.db import models
from accounts.models import User
from django.contrib.auth import get_user_model
from django.urls import reverse

# getting user model object
User = get_user_model()

class Task(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    complete = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def get_absolute_api_url(self):
        return reverse('todo:api-v1:task-detail', kwargs={'pk': self.pk})

    class Meta:
        order_with_respect_to = "author"
