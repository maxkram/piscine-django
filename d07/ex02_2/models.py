from django.db import models
from django.contrib.auth.models import User

class Tip(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Tip by {self.author.username} on {self.date}"