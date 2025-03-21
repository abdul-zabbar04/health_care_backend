from django.db import models

# Create your models here.

class Contact(models.Model):
    name= models.CharField(max_length=50)
    email= models.EmailField()
    message= models.TextField(max_length=250)
    on_create= models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    class Meta:
        ordering= ['on_create']

class Newsletter(models.Model):
    email= models.EmailField()
    on_create= models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.email