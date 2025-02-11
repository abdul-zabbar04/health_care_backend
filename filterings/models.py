from django.db import models

class Specialization(models.Model):
    name= models.CharField(max_length=50)
    slug= models.SlugField(max_length=55, null=True, blank=True)
    def __str__(self):
        return self.name
    
class HealthConcern(models.Model):
    name= models.CharField(max_length=50)
    def __str__(self):
        return self.name

class District(models.Model):
    name= models.CharField(max_length=50)
    class Meta:
        ordering= ['name']
    def __str__(self):
        return self.name

class Sub_district(models.Model):
    name= models.CharField(max_length=50)
    class Meta:
        ordering= ['name']
    def __str__(self):
        return self.name