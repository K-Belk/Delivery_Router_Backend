from rest_framework import routers
from .views import AddressesVewSet, CityStateVewSet, DeliveryViewSet, LocationsVewSet, GoogleApiKeyViewSet,RoutingKeyViewSet, MapKeyViewSet

router = routers.DefaultRouter()
router.register(r'locations', LocationsVewSet)
router.register(r'addresses', AddressesVewSet)
router.register(r'city-state', CityStateVewSet)
router.register(r'deliveries', DeliveryViewSet)
router.register(r'google-key', GoogleApiKeyViewSet, basename='key')
router.register(r'routing-key', RoutingKeyViewSet, basename='key')
router.register(r'map-key', MapKeyViewSet, basename='key')
urlpatterns = router.urls