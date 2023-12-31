from django.contrib.auth import login, get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import views as auth_views
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic as views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.templatetags.static import static
from django.views.decorators.cache import never_cache

from .forms import UserProfileForm, ContactForm, SellerReplyForm
from campstore.store.forms import ProductCreateForm, CategoryForm
from campstore.store.models import Product, OrderItem, Order, Category, ProductImage
from campstore.user_profile.models import UserProfileModel, ContactMessage, SellerReply
from django.forms import modelformset_factory
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages


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

            profile = user.userprofile

            return redirect(reverse('edit-profile', kwargs={'pk': profile.pk}))
    else:
        form = UserCreationForm()

    context = {
        'form': form
    }

    return render(request, 'user_profile/sign_up.html', context)


class CustomLoginUserView(auth_views.LoginView):
    template_name = 'user_profile/log_in.html'

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password. Please try again.')
        return super().form_invalid(form)


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
def seller_dashboard(request):
    seller_orders = OrderItem.objects.filter(product__user=request.user)
    context = {
        'seller_orders': seller_orders,
    }
    return render(request, 'store/seller_dashboard.html', context)


@login_required
def my_store_order_details(request, pk):
    order = get_object_or_404(Order, pk=pk)
    context = {
        'order': order
    }
    return render(request, 'user_profile/my_store_order_detail.html', context)


@login_required
def add_product(request):
    image_form_set = modelformset_factory(ProductImage, fields=('image',), extra=5, max_num=5)

    if request.method == 'POST':
        form = ProductCreateForm(request.POST, request.FILES)
        formset = image_form_set(request.POST, request.FILES, queryset=ProductImage.objects.none())

        if form.is_valid() and formset.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()

            for form in formset.cleaned_data:
                if form:
                    image = form['image']
                    ProductImage.objects.create(product=product, image=image)

            messages.success(request, 'The product was added successfully!')

            return redirect('my-store')
    else:
        form = ProductCreateForm()
        formset = image_form_set(queryset=ProductImage.objects.none())

    context = {
        'form': form,
        'formset': formset,
        'title': 'Add product',
    }
    return render(request, 'user_profile/add_product.html', context)


@login_required
def edit_product(request, pk):
    image_form_set = modelformset_factory(ProductImage, fields=('image',), extra=5, max_num=5)
    product = Product.objects.filter(user=request.user).get(pk=pk)
    if request.method == 'POST':
        form = ProductCreateForm(request.POST, request.FILES, instance=product)
        formset = image_form_set(request.POST, request.FILES, queryset=ProductImage.objects.none())
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()

            messages.success(request, 'Changes were made!')

            return redirect('my-store')
    else:
        form = ProductCreateForm(instance=product)
        formset = image_form_set(queryset=ProductImage.objects.filter(product=product))

    context = {
        'form': form,
        'title': 'Edit product',
        'formset': formset,
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


def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('my-account')
        else:
            print(form.errors)
    else:
        form = PasswordChangeForm(user=request.user)

    context = {'form': form}

    return render(request, 'user_profile/change_password.html', context)



@login_required
def contact_seller(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    seller = product.user

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = seller
            message.product = product
            message.save()
            messages.success(request, 'Your message has been sent to the seller.')
            return redirect('product-details', category_slug=product.category.slug, slug=product.slug)
    else:
        form = ContactForm()

    context = {
        'form': form,
        'product': product,
        'seller': seller,
    }
    return render(request, 'store/contact_seller.html', context)


@login_required
def seller_messages(request):
    messages_received = ContactMessage.objects.filter(receiver=request.user).order_by('-timestamp')

    context = {
        'messages_received': messages_received,
    }
    return render(request, 'store/seller_messages.html', context)


@login_required
def reply_to_sender(request, message_id):
    message = get_object_or_404(ContactMessage, pk=message_id)
    if request.method == 'POST':
        form = SellerReplyForm(request.POST)
        if form.is_valid():
            reply_message = form.cleaned_data['reply_message']
            reply = SellerReply.objects.create(message=message, sender=request.user, reply_message=reply_message)
            return redirect('seller-messages')
    else:
        form = SellerReplyForm()

    context = {
        'message': message,
        'form': form,
    }
    return render(request, 'store/reply_to_sender.html', context)


@login_required
def view_reply(request, message_id):
    message = get_object_or_404(ContactMessage, pk=message_id)
    context = {
        'message': message,
    }
    return render(request, 'store/view_reply.html', context)


@login_required
def sent_messages(request):
    sent_messages = ContactMessage.objects.filter(sender=request.user)
    context = {
        'sent_messages': sent_messages,
    }
    return render(request, 'store/sent_messages.html', context)