from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search, name='search'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add-to-cart'),
    path('change-quantity-cart/<str:product_id>/', views.change_quantity, name='change-quantity'),
    path('remove-from-cart/<str:product_id>/', views.remove_from_cart, name='remove-from-cart'),
    path('cart/', views.cart_details_view, name='cart-details'),
    path('cart/checkout/', views.checkout_view, name='checkout'),
    path('<slug:slug>/', views.category_details, name='category-details'),
    path('<slug:category_slug>/<slug:slug>/', views.product_details, name='product-details'),
]