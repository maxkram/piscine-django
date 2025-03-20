# from django.db import models

# class Planets(models.Model):
#     name = models.CharField(max_length=64, unique=True, null=False)
#     climate = models.CharField(max_length=255, null=True, blank=True)
#     diameter = models.IntegerField(null=True, blank=True)
#     orbital_period = models.IntegerField(null=True, blank=True)
#     population = models.BigIntegerField(null=True, blank=True)
#     rotation_period = models.IntegerField(null=True, blank=True)
#     surface_water = models.FloatField(null=True, blank=True)
#     terrain = models.CharField(max_length=255, null=True, blank=True)
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.name

# class People(models.Model):
#     name = models.CharField(max_length=64, null=False)
#     birth_year = models.CharField(max_length=32, null=True, blank=True)
#     gender = models.CharField(max_length=32, null=True, blank=True)
#     eye_color = models.CharField(max_length=32, null=True, blank=True)
#     hair_color = models.CharField(max_length=32, null=True, blank=True)
#     height = models.IntegerField(null=True, blank=True)
#     mass = models.FloatField(null=True, blank=True)
#     homeworld = models.ForeignKey(Planets, on_delete=models.SET_NULL, null=True, blank=True, to_field='name')
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.name


from django.db import models

# Create your models here.

class Planets(models.Model):
    class Meta:
        db_table = 'ex09_planets'
    name = models.CharField(max_length=64, unique=True)
    climate = models.CharField(max_length=64, null=True)
    diameter = models.IntegerField(null=True)
    orbital_period = models.IntegerField(null=True)
    population = models.BigIntegerField(null=True)
    rotation_period = models.IntegerField(null=True)
    surface_water = models.FloatField(null=True)
    terrain = models.CharField(max_length=128, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.name

class People(models.Model):
    class Meta:
        db_table = 'ex09_people'
    name = models.CharField(max_length=64, unique=True)
    birth_year = models.CharField(max_length=32, null=True)
    gender = models.CharField(max_length=32, null=True)
    eye_color = models.CharField(max_length=32, null=True)
    hair_color = models.CharField(max_length=32, null=True)
    height = models.IntegerField(null=True)
    mass = models.FloatField(null=True)
    homeworld = models.ForeignKey(Planets, on_delete=models.CASCADE, related_name='residents', null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.name