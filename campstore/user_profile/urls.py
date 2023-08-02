from django.urls import path, include
from . import views

urlpatterns = [
    path('signup/', views.sign_up_view, name='signup'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', views.LogoutUserView.as_view(), name='logout'),
    path('contact-seller/<int:product_id>/', views.contact_seller, name='contact-seller'),
    path('seller-messages/', views.seller_messages, name='seller-messages'),
    path('seller-messages/<int:message_id>/reply/', views.reply_to_sender, name='reply-to-sender'),
    path('sent-messages/', views.sent_messages, name='sent-messages'),
    path('view-reply/<int:message_id>/', views.view_reply, name='view-reply'),
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