from django.db import models
from django.db.models import CharField, SET_NULL
from django.forms import IntegerField


# Create your models here.
class Customer(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=320)
    pincode=models.IntegerField()
    create_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'

class Order(models.Model):
    customer = models.ForeignKey(Customer,related_name='order',on_delete=models.SET_NULL, null=True, blank=True)
    item_name= models.CharField(max_length=100)


class Author(models.Model):
    name = CharField(max_length=200)

    def __str__(self):
        return self.name

class Blog(models.Model):
    title = models.CharField(max_length=200,unique=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL,related_name='blogs',related_query_name='author_name', null=True, blank=True)
    content = models.TextField(blank=True)

    def __str__(self):
        return self.title

class Todo(models.Model):
    title = models.CharField(max_length=100)
    desc = models.TextField(null=True)
    status = models.BooleanField(default=False)


