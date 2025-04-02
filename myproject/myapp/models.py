from django.db import models
from accounts.models import CustomUser

class Tip(models.Model):
    content = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.content} by {self.author}"

    @property
    def upvote_count(self):
        return self.vote_set.filter(vote_type=Vote.UPVOTE).count()

    @property
    def downvote_count(self):
        return self.vote_set.filter(vote_type=Vote.DOWNVOTE).count()

    class Meta:
        permissions = [
            ('can_delete_tip', 'Can delete any tip'),
            ('downvote_tip', 'Can downvote any tip'),
        ]

class Vote(models.Model):
    UPVOTE = 'upvote'
    DOWNVOTE = 'downvote'
    VOTE_TYPES = (
        (UPVOTE, 'Upvote'),
        (DOWNVOTE, 'Downvote'),
    )
    tip = models.ForeignKey(Tip, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=10, choices=VOTE_TYPES)

    class Meta:
        unique_together = ('tip', 'user')

    def __str__(self):
        return f"{self.user} {self.vote_type}d {self.tip}"