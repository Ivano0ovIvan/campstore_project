from django.urls import path, include
from . import views

urlpatterns = [
    path('signup/', views.sign_up_view, name='signup'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', views.LogoutUserView.as_view(), name='logout'),
    path('my-account/', views.my_account, name='my-account'),
    path('my-store/', include([
        path('', views.my_store, name='my-store'),
        path('add_product/', views.add_product, name='add-product'),
        path('edit_product/<int:pk>/', views.edit_product, name='edit-product'),
        path('delete_product/<int:pk>/', views.delete_product, name='delete-product'),
    ])),
    path('sellers/<int:pk>/', views.SellerDetailsView.as_view(), name='seller-details')
]