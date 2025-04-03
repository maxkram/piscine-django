from django.db import models
from accounts.models import CustomUser

class Tip(models.Model):
    content = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    upvotes = models.ManyToManyField(CustomUser, related_name='upvoted_tips', blank=True)
    downvotes = models.ManyToManyField(CustomUser, related_name='downvoted_tips', blank=True)

    def __str__(self):
        return f"Tip by {self.author.username} - {self.created_at}"

    def get_upvote_count(self):
        return self.upvotes.count()

    def get_downvote_count(self):
        return self.downvotes.count()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.author.update_reputation()

    def delete(self, *args, **kwargs):
        author = self.author
        super().delete(*args, **kwargs)
        author.update_reputation()

    class Meta:
        permissions = [
            ("can_delete_tips", "Can delete any tip"),
            ("can_downvote_tips", "Can downvote any tip"),
        ]
        

# from django.db import models
# from django.contrib.auth.models import User

# class Tip(models.Model):
#     content = models.TextField()
#     author = models.ForeignKey(User, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     upvotes = models.ManyToManyField(User, related_name='upvoted_tips', blank=True)
#     downvotes = models.ManyToManyField(User, related_name='downvoted_tips', blank=True)

#     def __str__(self):
#         return f"Tip by {self.author.username} - {self.created_at}"

#     def get_upvote_count(self):
#         return self.upvotes.count()

#     def get_downvote_count(self):
#         return self.downvotes.count()

#     class Meta:
#         permissions = [
#             ("can_delete_tips", "Can delete any tip"),
#             ("can_downvote_tips", "Can downvote any tip"),
#         ]