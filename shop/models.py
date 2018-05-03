from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Product(models.Model):
    choices = (
        ('bouquet', 'Bouquet'),
        ('present', 'Present'),
        ('composition', 'Composition'),)
    name = models.CharField(max_length=200)
    quantity = models.IntegerField()
    price = models.FloatField()
    description = models.TextField(max_length=1000)
    available = models.BooleanField(default=False)
    category = models.CharField(max_length=1, choices=choices, default='b')
    # feedback = models.ForeignKey('Feedback', on_delete=models.SET_NULL, null=True, blank=True)
    img_1 = models.ImageField(upload_to='products/img')
    img_2 = models.ImageField(upload_to='shop/static/img/products', blank=True)
    img_3 = models.ImageField(upload_to='shop/static/img/products', blank=True)
    img_4 = models.ImageField(upload_to='shop/static/img/products', blank=True)
    label = models.CharField(max_length=10,
                             choices=(
                                 ('item_new', 'n'), ('item_hit', 'h'), ('item_action', 'a'),
                                 (' ', '')),
                             default=' ')

    def __str__(self):
        return self.name


# class Category(models.Model):
#     choices = (
#         ('b', 'Bouquet'),
#         ('p', 'Present'),
#         ('c', 'Composition'),)
#
#     category = models.CharField(max_length=1, choices=choices)


class Feedback(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    text = models.TextField(max_length=300)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField(auto_now=True)
    rating = models.IntegerField(choices=((1, 1), (2, 2), (3, 3), (4, 4), (5, 5)), default=5)

    class Meta:
        ordering = ['date']
