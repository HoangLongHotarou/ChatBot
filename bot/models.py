from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=10000)
    parent = models.ForeignKey('Category',on_delete=models.SET_NULL, null=True)

class Type(models.Model):
    name = models.CharField(max_length=200)

class Answer(models.Model):
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)