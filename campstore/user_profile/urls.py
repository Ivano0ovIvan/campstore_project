from django.urls import path, include
from . import views

urlpatterns = [
    path('signup/', views.sign_up_view, name='signup'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', views.LogoutUserView.as_view(), name='logout'),
    path('my-account/', include([
        path('', views.my_account, name='my-account'),
        path('edit-profile/<int:pk>/', views.UserProfileUpdateView.as_view(), name='edit-profile'),
    ])),
    path('my-store/', include([
        path('', views.my_store, name='my-store'),
        path('order-detail/<int:pk>/', views.my_store_order_details, name='my-store-order-details'),
        path('add-product/', views.add_product, name='add-product'),
        path('edit-product/<int:pk>/', views.edit_product, name='edit-product'),
        path('delete-product/<int:pk>/', views.delete_product, name='delete-product'),
        path('add-category/', views.AddCategoryView.as_view(), name='add-category'),
        path('edit-category/<slug:slug>/', views.EditCategoryView.as_view(), name='edit-category'),
        path('delete-category/<slug:slug>/', views.DeleteCategoryView.as_view(), name='delete-category'),
    ])),
    path('sellers/<int:pk>/', views.SellerDetailsView.as_view(), name='seller-details')
]