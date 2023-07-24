from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import views as auth_views
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import generic as views

from campstore.store.forms import ProductForm
from campstore.store.models import Product, Category
from campstore.user_profile.models import UserProfileModel


UserModel = get_user_model()


class SellerDetailsView(views.DetailView):
    template_name = 'user_profile/seller_details.html'
    model = UserModel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.filter(status=Product.ACTIVE)
        context['products'] = products

        return context


def sign_up_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)
            userprofile = UserProfileModel.objects.create(user=user)

            return redirect('frontpage')

    else:
        form = UserCreationForm()

    context = {
        'form': form
    }

    return render(request, 'user_profile/sign_up.html', context)


class LoginUserView(auth_views.LoginView):
    template_name = 'user_profile/log_in.html'


class LogoutUserView(auth_views.LogoutView):
    pass


@login_required
def my_account(request):
    return render(request, 'user_profile/my_account.html')


@login_required
def my_store(request):
    products = request.user.products.exclude(status=Product.DELETED)
    context = {
        'products': products
    }
    return render(request, 'user_profile/my_store.html', context)


@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()

            messages.success(request, 'The product was added successfully!')

            return redirect('my-store')
    else:
        form = ProductForm()

    context = {
        'form': form,
        'title': 'Add product'
    }
    return render(request, 'user_profile/add_product.html', context)


@login_required
def edit_product(request, pk):
    product = Product.objects.filter(user=request.user).get(pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            form.save()

            messages.success(request, 'Changes were made!')

            return redirect('my-store')
    else:
        form = ProductForm(instance=product)

    context = {
        'form': form,
        'title': 'Edit product',
        'product': product
    }
    return render(request, 'user_profile/add_product.html', context)


@login_required
def delete_product(request, pk):
    product = Product.objects.filter(user=request.user).get(pk=pk)
    product.status = Product.DELETED
    product.save()

    messages.success(request, 'The product was deleted!')

    return redirect('my-store')