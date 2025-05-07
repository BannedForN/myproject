from rest_framework import serializers
from firstproject.models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = '__all__'

class DesignerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designer
        fields = '__all__'

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'