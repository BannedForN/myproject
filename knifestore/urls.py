from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/login/', user_login, name='login'),
    path('auth/register/', user_registration, name='register'),
    path('logout/', user_logout, name='logout'),
    path('', home, name='home'),

    path('knife_list/', KnifeListView.as_view(), name='knife_list'),
    path('knives/create//', KnifeCreateView.as_view(), name='knife_create'),
    path('knives/<int:pk>/', KnifeDetailView.as_view(), name='knife_detail'),
    path('knives/<int:pk>/update/', KnifeUpdateView.as_view(), name='knife_update'),
    path('knives/<int:pk>/delete/', KnifeDeleteView.as_view(), name='knife_delete'),
    path('store/', KnifeStoreView.as_view(), name='knife_store'),

    path('category_list/', CategoryListView.as_view(), name='category_list'),
    path('categories/create/', CategoryCreateView.as_view(), name='category_create'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
    path('categories/<int:pk>/update/', CategoryUpdateView.as_view(), name='category_update'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),

    path('brand_list/', BrandListView.as_view(), name='brand_list'),
    path('brands/create/', BrandCreateView.as_view(), name='brand_create'),
    path('brands/<int:pk>/', BrandDetailView.as_view(), name='brand_detail'),
    path('brands/<int:pk>/update/', BrandUpdateView.as_view(), name='brand_update'),
    path('brands/<int:pk>/delete/', BrandDeleteView.as_view(), name='brand_delete'),

    path('series/', SeriesListView.as_view(), name='series_list'),
    path('series/create/', SeriesCreateView.as_view(), name='series_create'),
    path('series/<int:pk>/', SeriesDetailView.as_view(), name='series_detail'),
    path('series/<int:pk>/update/', SeriesUpdateView.as_view(), name='series_update'),
    path('series/<int:pk>/delete/', SeriesDeleteView.as_view(), name='series_delete'),

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
