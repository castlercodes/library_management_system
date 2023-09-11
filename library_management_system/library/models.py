from django.db import models
from django.contrib.auth.models import User

class UserProile(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    email = models.EmailField()
    address = models.TextField()
    college = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    author = models.CharField(max_length=100)
    image = models.CharField(max_length=1000)
    category = models.CharField(max_length=255)
    checkedOut = models.BooleanField(default=False)
    checkOutTime = models.CharField(max_length=100, default="19/2/2003")
    checkOutUser = models.CharField(max_length=255, default="No User")

    def __str__(self):
        return self.title