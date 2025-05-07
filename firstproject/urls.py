from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/login/', user_login, name='login'),
    path('auth/register/', user_registration, name='register'),
    path('logout/', user_logout, name='logout'),
    path('', home, name='home'),

    path('game_list/', GameListView.as_view(), name='game_list'),
    path('games/create//', GameCreateView.as_view(), name='game_create'),
    path('games/<int:pk>/', GameDetailView.as_view(), name='game_detail'),
    path('games/<int:pk>/update/', GameUpdateView.as_view(), name='game_update'),
    path('games/<int:pk>/delete/', GameDeleteView.as_view(), name='game_delete'),
    path('store/', GameStoreView.as_view(), name='game_store'),

    path('category_list/', CategoryListView.as_view(), name='category_list'),
    path('categories/create/', CategoryCreateView.as_view(), name='category_create'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
    path('categories/<int:pk>/update/', CategoryUpdateView.as_view(), name='category_update'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),

    path('publisher_list/', PublisherListView.as_view(), name='publisher_list'),
    path('publishers/create/', PublisherCreateView.as_view(), name='publisher_create'),
    path('publishers/<int:pk>/', PublisherDetailView.as_view(), name='publisher_detail'),
    path('publishers/<int:pk>/update/', PublisherUpdateView.as_view(), name='publisher_update'),
    path('publishers/<int:pk>/delete/', PublisherDeleteView.as_view(), name='publisher_delete'),

    path('designers/', DesignerListView.as_view(), name='designer_list'),
    path('designers/create/', DesignerCreateView.as_view(), name='designer_create'),
    path('designers/<int:pk>/', DesignerDetailView.as_view(), name='designer_detail'),
    path('designers/<int:pk>/update/', DesignerUpdateView.as_view(), name='designer_update'),
    path('designers/<int:pk>/delete/', DesignerDeleteView.as_view(), name='designer_delete'),

    path('customer_list', CustomerListView.as_view(), name='customer_list'),
    path('customers/create/', CustomerCreateView.as_view(), name='customer_create'),
    path('customers/<int:pk>/', CustomerDetailView.as_view(), name='customer_detail'),
    path('customers/<int:pk>/update/', CustomerUpdateView.as_view(), name='customer_update'),
    path('customers/<int:pk>/delete/', CustomerDeleteView.as_view(), name='customer_delete'),

    path('order_list', OrderListView.as_view(), name='order_list'),
    path('orders/create/', OrderCreateView.as_view(), name='order_create'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('orders/<int:pk>/update/', OrderUpdateView.as_view(), name='order_update'),
    path('orders/<int:pk>/delete/', OrderDeleteView.as_view(), name='order_delete'),
    path('my_orders/', user_orders, name='user_orders'),

    path('order-items/', OrderItemListView.as_view(), name='orderitem_list'),
    path('order-items/create/', OrderItemCreateView.as_view(), name='orderitem_create'),
    path('order-items/<int:pk>/', OrderItemDetailView.as_view(), name='orderitem_detail'),
    path('order-items/<int:pk>/update/', OrderItemUpdateView.as_view(), name='orderitem_update'),
    path('order-items/<int:pk>/delete/', OrderItemDeleteView.as_view(), name='orderitem_delete'),

    path('stock/', StockListView.as_view(), name='stock_list'),
    path('stock/create/', StockCreateView.as_view(), name='stock_create'),
    path('stock/<int:pk>/update/', StockUpdateView.as_view(), name='stock_update'),
    path('stock/<int:pk>/delete/', StockDeleteView.as_view(), name='stock_delete'),
]
