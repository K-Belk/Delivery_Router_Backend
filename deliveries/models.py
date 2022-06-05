from django.db import models
from django.conf import settings

class City_State(models.Model):
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=15)
    postal_code = models.CharField(max_length=5)
    class meta:
        unique_together = ('city', 'state', 'postal_code')
    
class Addresses(models.Model):
    street = models.CharField(max_length=200)
    suite = models.CharField(max_length=10, blank=True)
    city_and_state = models.ForeignKey(City_State, on_delete=models.CASCADE, related_name='city_and_state')
    latitude = models.CharField(max_length=200)
    longitude = models.CharField(max_length=200)
    notes = models.TextField(blank=True)

class Delivery_Location(models.Model):
    name = models.CharField(max_length=200)
    address = models.ForeignKey(Addresses, on_delete=models.CASCADE, related_name='addresses')

    class meta:
        unique_together = ('name', 'address')

class Deliveries(models.Model):
    driver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lnk_delivery = models.IntegerField(null=True)
    fifty_five_delivery = models.IntegerField(null=True)
    date = models.DateField(null=True)
    location = models.ForeignKey(Addresses, on_delete=models.CASCADE ,related_name='delivery')
    

class Delivery_Season(models.Model):
    season = models.CharField(max_length=200)
    year = models.DateField
    delivery = models.ForeignKey(Deliveries, on_delete=models.CASCADE, related_name='delivery_season')

