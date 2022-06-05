from rest_framework import routers
from .views import AddressesVewSet, CityStateVewSet, LocationsVewSet

router = routers.DefaultRouter()
router.register(r'locations', LocationsVewSet)
router.register(r'addresses', AddressesVewSet)
router.register(r'city-state', CityStateVewSet)
urlpatterns = router.urls