from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import Permission
from .models import CustomUser
from myapp.models import Vote, Tip

@receiver(post_save, sender=Vote)
def update_reputation_on_vote(sender, instance, created, **kwargs):
    if created:
        author = instance.tip.author
        if instance.vote_type == Vote.UPVOTE:
            author.reputation += 5
        elif instance.vote_type == Vote.DOWNVOTE:
            author.reputation -= 2
        author.save()

@receiver(post_delete, sender=Vote)
def update_reputation_on_vote_delete(sender, instance, **kwargs):
    author = instance.tip.author
    if instance.vote_type == Vote.UPVOTE:
        author.reputation -= 5
    elif instance.vote_type == Vote.DOWNVOTE:
        author.reputation += 2
    author.save()

@receiver(post_save, sender=CustomUser)
def update_permissions(sender, instance, **kwargs):
    downvote_perm = Permission.objects.get(codename='downvote_tip')
    delete_perm = Permission.objects.get(codename='delete_tip')
    if instance.reputation >= 15:
        instance.user_permissions.add(downvote_perm)
    else:
        instance.user_permissions.remove(downvote_perm)
    if instance.reputation >= 30:
        instance.user_permissions.add(delete_perm)
    else:
        instance.user_permissions.remove(delete_perm)