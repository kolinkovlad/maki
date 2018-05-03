from django.conf.urls.static import static

from maki import settings
from . import views
from django.urls import include, path

app_name = 'shop'

urlpatterns = [path('homepage/', views.HomePage.as_view(), name='homeview'),
               path('product/<int:pk>', views.ProductDetail.as_view(), name='product-detail'),
               path('save_feedback/', views.save_feedback, name='save-feedback'),
               path('add_to_basket/<int:pk>', views.add_to_basket, name='add-to-basket'),

               ]
