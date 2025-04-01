from django.db import models
from django.contrib.auth.models import User

class Tip(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    upvotes = models.ManyToManyField(User, related_name='upvoted_tips', blank=True)
    downvotes = models.ManyToManyField(User, related_name='downvoted_tips', blank=True)

    def __str__(self):
        return f"Tip by {self.author.username} on {self.date}"

    def upvote_count(self):
        return self.upvotes.count()

    def downvote_count(self):
        return self.downvotes.count()