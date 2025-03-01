from django.db import models

class Movies(models.Model):
    # Fields
    episode_nb = models.AutoField(primary_key=True)  # Primary key
    title = models.CharField(max_length=64, unique=True, null=False)  # Unique, max 64 chars, non-null
    opening_crawl = models.TextField(null=True, blank=True)  # Text, can be null
    director = models.CharField(max_length=32, null=False)  # Max 32 chars, non-null
    producer = models.CharField(max_length=128, null=False)  # Max 128 chars, non-null
    release_date = models.DateField(null=False)  # Date, non-null

    # Override __str__ method
    def __str__(self):
        return self.title

    class Meta:
        db_table = 'ex00_schema.movies'  # Use the same schema as ex00