from .views import *
from rest_framework import routers

urlpatterns = [

]

router = routers.SimpleRouter()

router = routers.DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('publishers', PublisherViewSet, basename='publishers')
router.register('designers', DesignerViewSet, basename='designers')
router.register('games', GameViewSet, basename='games')
router.register('customers', CustomerViewSet, basename='customers')
router.register('orders', OrderViewSet, basename='orders')
router.register('orderitems', OrderItemViewSet, basename='orderitems')
router.register('stocks', StockViewSet, basename='stocks')
urlpatterns += router.urls