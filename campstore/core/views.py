from campstore.store.models import Product, Category
from django.views import generic as views
from django.shortcuts import render


class ProductListView(views.ListView):
    template_name = 'core/frontpage.html'
    model = Product
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        queryset = Product.objects.filter(status=Product.ACTIVE)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, *kwargs)
        context['categories'] = Category.objects.all()
        return context


def page_not_found(request, exception):
    return render(request, '404.html', status=404)
