from django.db import models
from django.contrib.auth.models import AbstractUser
# Remove: from tips.models import Tip

class CustomUser(AbstractUser):
    reputation = models.IntegerField(default=0)

    def update_reputation(self):
        # Calculate reputation: +5 per upvote, -2 per downvote on user's tips
        tips = self.tip_set.all()
        upvotes = sum(tip.upvotes.count() for tip in tips)
        downvotes = sum(tip.downvotes.count() for tip in tips)
        self.reputation = (upvotes * 5) - (downvotes * 2)
        self.save()

        # Update permissions based on reputation
        from django.contrib.auth.models import Permission
        from django.contrib.contenttypes.models import ContentType
        
        # Use string reference to avoid direct import
        tip_content_type = ContentType.objects.get(app_label='tips', model='tip')
        
        # Downvote permission at 15 points
        downvote_perm = Permission.objects.get(
            codename='can_downvote_tips',
            content_type=tip_content_type
        )
        if self.reputation >= 15:
            self.user_permissions.add(downvote_perm)
        else:
            self.user_permissions.remove(downvote_perm)
            
        # Delete permission at 30 points
        delete_perm = Permission.objects.get(
            codename='can_delete_tips',
            content_type=tip_content_type
        )
        if self.reputation >= 30:
            self.user_permissions.add(delete_perm)
        else:
            self.user_permissions.remove(delete_perm)

    def __str__(self):
        return self.username