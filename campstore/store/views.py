from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic as views
from .models import Product, Category, Order, OrderItem
from .forms import OrderForm
from .cart import Cart
from ..user_profile.models import UserProfileModel


def search(request):
    query = request.GET.get('query', '')
    products = Product.objects.filter(status=Product.ACTIVE).filter(
        Q(title__icontains=query) | Q(description__icontains=query))
    context = {
        'query': query,
        'products': products
    }

    return render(request, 'store/search.html', context)


def category_details(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.filter(status=Product.ACTIVE)
    context = {
        'category': category,
        'products': products
    }
    return render(request, 'store/category_details.html', context)


def product_details(request, category_slug, slug):
    product = get_object_or_404(Product, slug=slug, status=Product.ACTIVE)
    context = {
        'product': product
    }

    return render(request, 'store/product_details.html', context)


def add_to_cart(request, product_id):
    cart = Cart(request)
    cart.add(product_id)

    return redirect('frontpage')


def cart_details_view(request):
    cart = Cart(request)

    context = {
        'cart': cart
    }

    return render(request, 'store/cart_details.html', context)


@login_required
def checkout_view(request):
    cart = Cart(request)

    if request.method == 'POST':
        form = OrderForm(request.POST)

        if form.is_valid():
            total_price = 0

            for item in cart:
                product = item['product']
                quantity = int(item['quantity'])
                total_price += product.price * quantity
                if quantity > product.quantity:
                    messages.error(request,
                                   f"Sorry, there are only {product.quantity} units available for '{product.title}'.")
                    return redirect('checkout')
                else:
                    if quantity == product.quantity:
                        product.status = product.status = Product.SOLD_OUT
                        product.save()
            order = form.save(commit=False)
            order.created_by = request.user
            order.paid_amount = total_price
            order.save()
            for item in cart:
                product = item['product']
                quantity = int(item['quantity'])
                price = product.price * quantity

                item = OrderItem.objects.create(
                    order=order,
                    product=product,
                    price=price,
                    quantity=quantity,
                )

                cart.clear()

            return redirect('my-account')
    else:
        form = OrderForm()

    context = {
        'cart': cart,
        'form': form,
        'messages': messages.get_messages(request)
    }
    return render(request, 'store/checkout.html', context)


def change_quantity(request, product_id):
    action = request.GET.get('action', '')

    if action:
        quantity = 1

        if action == 'decrease':
            quantity = -1

        cart = Cart(request)
        cart.add(product_id, quantity, True)

    return redirect('cart-details')


def remove_from_cart(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)

    return redirect('cart-details')
