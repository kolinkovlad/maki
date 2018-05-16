from django.conf.urls.static import static

from maki import settings
from . import views
from django.urls import include, path

app_name = 'shop'

urlpatterns = [path('homepage/', views.HomePage.as_view(), name='homeview'),
               path('product/<int:pk>', views.ProductDetail.as_view(), name='product-detail'),
               path('save_feedback/', views.save_feedback, name='save-feedback'),
               path('add_to_basket/<int:pk>', views.add_to_basket, name='add-to-basket'),
               path('add_to_basket_from_details/<int:pk>', views.add_to_basket_from_details, name='add-to-basket-from-details'),
               path('del_good_from_basket', views.del_good_from_basket, name='del-good-from-basket'),
               path('basket/', views.ProductBasket.as_view(), name='basket'),
               path('user_registration/', views.UserRegistration.as_view(), name='user-registration'),
               path('product_order/', views.ProductOrder.as_view(), name='product-order'),

               ]
