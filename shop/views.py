from django.shortcuts import render, render_to_response, redirect
from django.urls import reverse_lazy
from django.views import generic
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
class TopProductCookiesMixin:

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        quantity = 0
        sum = 0
        for item in self.request.session.keys():
            if 'good_' in item:
                q = int(self.request.session.get(item))
                id = int(item[5:])
                try:
                    good = Product.objects.get(pk=id)
                    price = good.price
                    quantity += q
                    sum += q * price
                except:
                    pass

        context['total_quantity'] = quantity
        context['sum'] = sum
        return context


class HomePage(TopProductCookiesMixin, generic.ListView):
    model = Product
    paginate_by = 4

    def listing(self):
        product_list = Product.objects.all()
        paginator = Paginator(product_list, 4)  # Show 4 contacts per page

    def get_queryset(self):
        result = super(HomePage, self).get_queryset()
        if self.request.GET.get('data_search'):
            result = result.filter(text__contains=self.request.GET.get('data_search'))
        return result

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(HomePage, self).get_context_data(**kwargs)
        quantity_goods = 0
        total_sum = 0
        for item in self.request.session.keys():
            if 'good_' in item:
                q = int(self.request.session.get(item))
                id_good = int(item[5:])
                try:
                    good = Product.objects.get(pk=id_good)
                    quantity_goods += q
                    total_sum += q * good.price
                except:
                    pass

        context['total_quantity'] = quantity_goods
        context['total_sum'] = total_sum
        return context


class ProductDetail(TopProductCookiesMixin, generic.DetailView):
    model = Product


def save_feedback(request):
    if request.POST:
        # print(request.POST)
        feedback = Feedback()
        feedback.user_id = int(request.POST['user_id'])
        feedback.product_id = int(request.POST['product_id'])
        feedback.text = request.POST['text']
        feedback.save()

        return redirect(to=request.POST['url'])
    else:
        redirect(to='/')


def add_to_basket(request, pk):
    good = 'good_' + str(pk)
    quantity = request.session.get(good, 0)
    request.session[good] = quantity + 1

    for item in request.session.keys():
        print(item, '=', request.session.get(item))
    return redirect(to='/shop/homepage/')


class Order(generic):
    pass