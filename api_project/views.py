from django.shortcuts import render

from .serializers import *
from rest_framework import viewsets, mixins
from firstproject.models import *
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

class PublisherViewSet(mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       viewsets.GenericViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    permission_classes = [CustomPermissions]
    pagination_class = PaginationPage
    renderer_classes = [AdminRenderer]

    def get_queryset(self):
        queryset = Publisher.objects.all()
        name = self.request.query_params.get('name', None)

        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        
        return queryset
    
class DesignerViewSet(viewsets.ModelViewSet):
    queryset = Designer.objects.all()
    serializer_class = DesignerSerializer
    permission_classes = [CustomPermissions]
    pagination_class = PaginationPage

    def get_queryset(self):
        queryset = Designer.objects.all()
        last_name = self.request.query_params.get('last_name', None)

        if last_name is not None:
            queryset = queryset.filter(last_name__icontains=last_name)
        
        return queryset

class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [CustomPermissions]
    pagination_class = PaginationPage

    def get_queryset(self):
        queryset = Game.objects.all()
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