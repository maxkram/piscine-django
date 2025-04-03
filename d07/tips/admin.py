from django.contrib import admin
from .models import Tip

@admin.register(Tip)
class TipAdmin(admin.ModelAdmin):
    list_display = ('content', 'author', 'created_at', 'get_upvote_count', 'get_downvote_count')