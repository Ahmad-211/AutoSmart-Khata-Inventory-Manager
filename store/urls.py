from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, PartViewSet, SaleViewSet

# The router automatically generates the URLs for our ViewSets
router = DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'parts', PartViewSet)
router.register(r'sales', SaleViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]