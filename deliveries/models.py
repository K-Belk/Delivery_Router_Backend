from django.db import models
from django.conf import settings
from django.core.validators import MinLengthValidator


class Delivery_Location(models.Model):
    name = models.CharField(max_length=200)
    street = models.CharField(max_length=200)
    suite = models.CharField(max_length=10, blank=True)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=2)
    postal_code = models.CharField(max_length=5, validators=[MinLengthValidator(5)])
    latitude = models.CharField(max_length=200)
    longitude = models.CharField(max_length=200)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together =('name','street', 'city', 'state', 'postal_code')

class ProductChoices(models.Model):
    product = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.product
        
class EditionChoices(models.Model):
    edition = models.CharField(max_length=200)
    year = models.IntegerField(unique_for_year=('year'))
    product = models.ForeignKey(ProductChoices, on_delete=models.CASCADE, related_name='product_choice_edition')

    def __str__(self):
        return self.edition + self.year + self.product

    class Meta:
        unique_together = ('edition', 'year', 'product')

class Deliveries(models.Model):
    driver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    edition = models.ForeignKey(EditionChoices, on_delete=models.CASCADE, related_name='edition_choice')
    product = models.ForeignKey(ProductChoices, on_delete=models.CASCADE, related_name='product_choice')
    amount = models.IntegerField()
    date = models.DateField(null=True)
    location = models.ForeignKey(Delivery_Location, on_delete=models.CASCADE ,related_name='delivery')
