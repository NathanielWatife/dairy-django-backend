from django.urls import path, include
from rest_framework import routers

from inventory.views import CowInventoryViewSet, CowInventoryUpdateHistoryViewSet

app_name = "inventory"


router = routers.DefaultRouter()
router.register(r'cow-inventory', CowInventoryViewSet, basename='cow-inventory')
router.register(r'cow-inventory-history', CowInventoryUpdateHistoryViewSet, basename='cow-inventory-history')


urlpatterns = [
    path("", include(router.urls)),
]
