from .views import *
from rest_framework import routers

urlpatterns = [

]

router = routers.SimpleRouter()

router = routers.DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('brands', BrandViewSet, basename='brands')
router.register('series', SeriesViewSet, basename='series')
router.register('knives', KnifeViewSet, basename='knives')
router.register('customers', CustomerViewSet, basename='customers')
router.register('orders', OrderViewSet, basename='orders')
router.register('orderitems', OrderItemViewSet, basename='orderitems')
router.register('stocks', StockViewSet, basename='stocks')
urlpatterns += router.urls