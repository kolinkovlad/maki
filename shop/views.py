from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseForbidden
from django.shortcuts import render, render_to_response, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import generic

from shop.forms import RegisterUserForm, AddToBasketFromDetails
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
        context['order'] = False
        return context


class HomePage(TopProductCookiesMixin, generic.ListView):
    model = Product
    paginate_by = 4

    def listing(self):
        product_list = Product.objects.all()
        paginator = Paginator(product_list, 4)  # Show 4 contacts per page

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

    def get_context_data(self, *, object_list=None, **kwargs):
        if self.request.GET.get('order_quantity'):
            print("GEEET")
            self.request.session['good_' + str(self.kwargs['pk'])] = int(self.request.GET.get('order_quantity'))
        context = super().get_context_data(object_list=None, **kwargs)
        context['quantity'] = self.request.session.get('good_' + str(self.kwargs['pk']), 1)
        return context

    # def get_queryset(self):
    #     result = super().get_queryset()
    #     result2 = Product.objects.all()
    #     return result2


def add_to_basket_from_details(request, pk):
    print(request.GET.get('order_quantity'))
    good = 'good_' + str(pk)
    quantity = request.session.get(good, 0)
    # request.session[good] = quantity + value_quantity


def save_feedback(request):
    if request.POST:
        # print(request.POST)
        feedback = Feedback()
        feedback.user_id = int(request.POST['user_id'])
        feedback.product_id = int(request.POST['product_id'])
        feedback.text = request.POST['text']

        if not Feedback.objects.filter(text__contains=request.POST['text']):
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


def del_good_from_basket(request):
    request.session.pop(request.GET.get('remove'))
    return redirect('shop:basket')


class ProductBasket(generic.TemplateView, TopProductCookiesMixin):
    template_name = 'basket.html'

    def get_context_data(self, **kwargs):

        context = super(ProductBasket, self).get_context_data(**kwargs)
        total_sum = 0
        goods = []

        for item in self.request.session.keys():
            if 'good_' not in item:
                continue
            quantity_goods = int(self.request.session.get(item))
            context['total_quantity'] = quantity_goods

            try:
                good = Product.objects.get(pk=int(item[5:]))
                summ = quantity_goods * good.price
                total_sum += summ
                goods.append((good, int(self.request.session.get(item)), summ))
            except:
                pass
        context['goods'] = goods
        context['total_sum'] = total_sum
        context['order'] = True
        return context


class ProductOrder(TopProductCookiesMixin, LoginRequiredMixin, generic.CreateView):
    template_name = 'product_order.html'
    model = Order
    form_class = OrderForm
    success_url = 'shop:product_list'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = True

        return context

    def form_valid(self, form):
        print(form.cleaned_data)

    def form_invalid(self, form):
        print("Form invalid")
        print(form.cleaned_data)

    # def save_to_database(self):


class UserRegistration(generic.CreateView):
    form_class = RegisterUserForm
    template_name = 'registration/user_registration.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseForbidden()

        return super(UserRegistration, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # print('form valid')
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        # print("_______", user)
        # login(request=self.request, user=user)
        # print("_______222222", user)
        # current_site = get_current_site(self.request)
        # subject = 'Activation of your account'
        # message = render_to_string('blog/acc_activate_email.html', {'user': user,
        #                                                             'domain': current_site.domain,
        #                                                             'uid': urlsafe_base64_encode(
        #                                                                 force_bytes(user.pk)).decode(),
        #                                                             'token': account_activation_token.make_token(
        #                                                                 user)})
        # to_email = form.cleaned_data['email']
        #
        # email = EmailMessage(subject, message, to=[to_email])
        # email.send()
        # messages.success(self.request, 'Please confirm account by your e-mail.')

        return redirect(to='/shop/homepage/')
