from django.contrib import admin

# Register your models here.
from shop.models import Product, Feedback

admin.site.register(Product)
# admin.site.register(Category)
admin.site.register(Feedback)
