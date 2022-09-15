from rest_framework import routers

from .views import (DeliveryViewSet, GoogleApiKeyViewSet, LocationsVewSet,
                    MapKeyViewSet, RoutingKeyViewSet, )

app_name= 'deliveries'

router = routers.DefaultRouter()
router.register(r'locations', LocationsVewSet, basename='locations')
router.register(r'deliveries', DeliveryViewSet)
router.register(r'google-key', GoogleApiKeyViewSet, basename='key')
router.register(r'routing-key', RoutingKeyViewSet, basename='key')
router.register(r'map-key', MapKeyViewSet, basename='key')
urlpatterns = router.urls
