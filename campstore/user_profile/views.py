from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import views as auth_views
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.templatetags.static import static
from .forms import UserProfileForm
from campstore.store.forms import ProductForm, CategoryForm
from campstore.store.models import Product, OrderItem, Order, Category
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

            UserProfileModel.objects.create(user=user)

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
    user_profile, created = UserProfileModel.objects.get_or_create(user=request.user)

    is_seller = user_profile.is_seller
    context = {
        'user_profile': user_profile,
        'is_seller': is_seller,
    }
    return render(request, 'user_profile/my_account.html', context)


@login_required
def my_store(request):
    products = request.user.products.exclude(status=Product.DELETED)
    order_items = OrderItem.objects.filter(product__user=request.user)
    categories = Category.objects.all()
    context = {
        'products': products,
        'order_items': order_items,
        'categories': categories
    }
    return render(request, 'user_profile/my_store.html', context)


@login_required
def my_store_order_details(request, pk):
    order = get_object_or_404(Order, pk=pk)
    context = {
        'order': order
    }
    return render(request, 'user_profile/my_store_order_detail.html', context)


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


class AddCategoryView(LoginRequiredMixin, views.CreateView):
    model = Category
    template_name = 'user_profile/add_category.html'
    form_class = CategoryForm
    success_url = reverse_lazy('my-store')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add category'

        return context

    def form_valid(self, form):
        messages.success(self.request, 'Category added successfully!')
        return super().form_valid(form)


class EditCategoryView(LoginRequiredMixin, views.UpdateView):
    model = Category
    template_name = 'user_profile/add_category.html'
    form_class = CategoryForm
    success_url = reverse_lazy('my-store')

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Category, slug=slug)

    def form_valid(self, form):
        messages.success(self.request, 'Category edited successfully!')
        return super().form_valid(form)


class DeleteCategoryView(LoginRequiredMixin, views.DeleteView):
    model = Category
    template_name = 'user_profile/delete_category.html'
    success_url = reverse_lazy('my-store')

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Category, slug=slug)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Category deleted successfully!')
        return super().delete(request, *args, **kwargs)


class UserProfileUpdateView(LoginRequiredMixin, views.UpdateView):
    model = UserProfileModel
    form_class = UserProfileForm
    template_name = 'user_profile/edit_profile.html'
    success_url = reverse_lazy('my-account')
    profile_picture = static('images/person.png')

    def get_profile_picture(self):
        if self.object.profile_picture is not None:
            return self.object.profile_picture

        return self.profile_picture

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_picture'] = self.get_profile_picture()

        return context

    def get_object(self, queryset=None):
        return self.request.user.userprofile

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.instance.user = self.request.user
        return form
