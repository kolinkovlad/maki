from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.forms import ModelForm


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


class Feedback(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    text = models.TextField(max_length=300)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField(auto_now=True)
    rating = models.IntegerField(choices=((1, 1), (2, 2), (3, 3), (4, 4), (5, 5)), default=5)

    class Meta:
        ordering = ['date']


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    order_date = models.DateTimeField(auto_now=True)
    payed = models.BooleanField(default=False)
    send = models.BooleanField(default=False)
    resive = models.BooleanField(default=False)
    order_sum = models.FloatField()
    recipient_phone = models.CharField(max_length=13)
    recipient_card = models.CharField(max_length=13)
    recipient_first_name = models.CharField(max_length=13)
    recipient_last_name = models.CharField(max_length=13)
    recipient_surname = models.CharField(max_length=13)
    recipient_city_address = models.CharField(max_length=13)
    recipient_local_address = models.CharField(max_length=13)
    add_free_message_card = models.BooleanField(max_length=13)
    free_message_card_text = models.TextField(max_length=100)
    delivery_datetime = models.DateTimeField()


class OrderForm(ModelForm):

    class Meta:
        model = Order
        exclude = ['order_date', 'send', 'payed']


class GoodsInOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    good = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    payment = models.CharField(choices=(('online', 'online'), ('cash_on', 'cash_on')), max_length=15, default='cash_on')
