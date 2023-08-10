from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.cache import never_cache

from .models import Product, Category, Order, OrderItem
from .forms import OrderForm
from .cart import Cart
from .. import settings


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

@never_cache
def product_details(request, category_slug, slug):
    product = get_object_or_404(Product, slug=slug, status=Product.ACTIVE)
    images = product.images_related.all()

    product.view_count += 1
    product.save()

    context = {
        'product': product,
        'images': images,
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
    User = get_user_model()

    user = request.user
    initial_data = {
        'first_name': user.userprofile.first_name,
        'last_name': user.userprofile.last_name,
        'address': user.userprofile.address,
        'post_code': user.userprofile.post_code,
        'phone_number': user.userprofile.phone_number,
    }

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
                    product.quantity -= quantity
                    if product.quantity == 0:
                        product.status = Product.WAITING_APPROVAL
                    product.save()
            order = form.save(commit=False)
            order.created_by = request.user
            order.paid_amount = total_price
            order.save()
            for item in cart:

                product = item['product']
                quantity = int(item['quantity'])
                price = product.price * quantity
                order_item = OrderItem.objects.create(
                    order=order,
                    product=product,
                    price=price,
                    quantity=quantity,
                )

                associated_product = order_item.product
                seller = associated_product.user.userprofile
                subject = 'New Purchase Notification'
                message = f'Hello {associated_product.user.username},\n\nYou have a new purchase for {associated_product.title}.\n\nOrder ID: {order.id}'
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [seller.email]
                send_mail(subject, message, from_email, recipient_list)

            cart.clear()

            messages.success(request, 'Your order has been sent for processing. Wait for confirmation from the seller!')

            return redirect('my-account')
    else:
        form = OrderForm(initial=initial_data)

    context = {
        'cart': cart,
        'form': form,
        'messages': messages.get_messages(request)
    }
    return render(request, 'store/checkout.html', context)


@login_required
def change_product_status(request, product_id):
    if request.method == 'POST':
        new_status = request.POST.get('status')
        product = get_object_or_404(Product, id=product_id)

        if new_status in [status for status, _ in Product.STATUS_CHOICES]:
            product.status = new_status
            product.save()
            messages.success(request, f"Product '{product.title}' status has been updated to '{product.get_status_display()}'.")
        else:
            messages.error(request, "Invalid status value.")

    return redirect('seller-dashboard')


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
