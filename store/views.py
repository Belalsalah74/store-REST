from django.db import transaction
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.views import generic
from .models import Product, Cart, CartItem, Order, OrderItem, Category


class ProductList(generic.ListView):
    model = Product
    paginate_by = 10


class ProductDetail(generic.DetailView):
    model = Product

    # def get(self,request,*args, **kwargs):
    #     product = self.object = self.get_object()
    #     context = self.get_context_data()
    #     if 'cart_id' in request.session:
    #         context['cart_id'] = request.session['cart_id']
    #     print(context)
    #     return render(request, 'store/product_detail.html', context)

    def post(self, request, *args, **kwargs):
        with transaction.atomic():
            cart_id = request.session.get('cart_id')
            product = self.object = self.get_object()
            quantity = int(request.POST.get('quantity'))
            cart, created = Cart.objects.get_or_create(pk=cart_id)

            if not created:
                try:
                    cartitem = CartItem.objects.get(product=product)
                    cartitem.quantity += quantity
                    cartitem.save()

                except CartItem.DoesNotExist:
                    CartItem.objects.create(
                        cart=cart, product=product, quantity=quantity)

            else:
                CartItem.objects.create(
                    cart=cart, product=product, quantity=quantity)
                request.session['cart_id'] = str(cart.pk)

            messages.success(request, 'Item added to cart')
            return redirect(product)



class CartDetail(generic.DetailView):
    model = Cart
    pk_url_kwarg = 'uuid'

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):

        with transaction.atomic():
            cart = self.get_object()
            customer = request.user.customer
            order = Order.objects.create(customer=customer)
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    item_price=item.product.price,
                    quantity=item.quantity
                )
            cart.delete()
            request.session.pop('cart_id')
            messages.success(request, 'Order created successfully')
            return redirect('/')


class OrderDetail(LoginRequiredMixin, generic.DetailView):
    model = Order


class OrderList(LoginRequiredMixin, generic.ListView):

    def get(self, request, *args, **kwargs):
        qs = Order.objects.filter(customer=request.user.customer)
        context = {'object_list': qs}
        return render(request, 'store/order_list.html', context)


class CategoryList(generic.ListView):
    model = Category


class CategoryDetail(generic.DetailView):
    model = Category


class ProductSearch(generic.ListView):

    def get(self, request):
        query = request.GET.get('query')
        if len(query) > 0:
            qs = Product.objects.filter(name__icontains=query)
        else:
            qs = Product.objects.none
        context = {'object_list': qs}
        return render(request, 'store/search.html', context)


class Index(generic.TemplateView):
    template_name = 'store/index.html'
