from model_bakery import baker

from ...deliveries.models import Delivery_Location, Deliveries, ProductChoices, EditionChoices

# create delivery location database and 3 instances
baker.make(Delivery_Location, _quantity=3)
