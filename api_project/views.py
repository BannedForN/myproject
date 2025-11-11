from django.shortcuts import render

from .serializers import *
from rest_framework import viewsets, mixins
from knifestore.models import *
from .permission import CustomPermissions, PaginationPage
from rest_framework.renderers import AdminRenderer
# Create your views here.
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [CustomPermissions]
    pagination_class = PaginationPage

    def get_queryset(self):
        queryset = Category.objects.all()
        name = self.request.query_params.get('name', None)

        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        
        return queryset

class BrandViewSet(mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       viewsets.GenericViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [CustomPermissions]
    pagination_class = PaginationPage
    renderer_classes = [AdminRenderer]

    def get_queryset(self):
        queryset = Brand.objects.all()
        name = self.request.query_params.get('name', None)

        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        
        return queryset
    
class SeriesViewSet(viewsets.ModelViewSet):
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer
    permission_classes = [CustomPermissions]
    pagination_class = PaginationPage

    def get_queryset(self):
        queryset = Series.objects.all()
        last_name = self.request.query_params.get('last_name', None)

        if last_name is not None:
            queryset = queryset.filter(last_name__icontains=last_name)
        
        return queryset

class KnifeViewSet(viewsets.ModelViewSet):
    queryset = Knife.objects.all()
    serializer_class = KnifeSerializer
    permission_classes = [CustomPermissions]
    pagination_class = PaginationPage

    def get_queryset(self):
        queryset = Knife.objects.all()
        title = self.request.query_params.get('title', None)

        if title is not None:
            queryset = queryset.filter(title__icontains=title)
        
        return queryset
    
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [CustomPermissions]
    pagination_class = PaginationPage
    
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [CustomPermissions]
    pagination_class = PaginationPage

    
class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [CustomPermissions]
    pagination_class = PaginationPage

    
class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [CustomPermissions]
    pagination_class = PaginationPage