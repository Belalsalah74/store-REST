from django.contrib import messages
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render, redirect
from django.views import generic
from .models import Product, Cart, CartItem, Order, OrderItem, Category, Customer


class ProductList(generic.ListView):
    model = Product
    paginate_by = 10


class ProductDetail(generic.DetailView):
    model = Product
    extra_context = {}

    def get(self,request,*args, **kwargs):
        product = self.object = self.get_object()
        context = self.get_context_data()
        if 'cart_id' in request.session:
            context['cart_id'] = request.session['cart_id']
        print(context)
        return render(request, 'store/product_detail.html', context)

    def post(self, request, *args, **kwargs):
        cart_id = request.session.get('cart_id')
        product = self.object =self.get_object()
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
            
        messages.success(request,'Item added to cart')
        return redirect(product)


class CartCreate(generic.CreateView):
    template_name = 'store/product_detail.html'
    model = Cart
    fields = []


class CartDetail(generic.DetailView):
    model = Cart
    pk_url_kwarg = 'uuid'


class Index(generic.TemplateView):
    template_name = 'store/index.html'
