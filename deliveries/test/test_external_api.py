import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from ..external_api_calls import ExternalApiCall

class ExternalApiTest(APITestCase):

    def setUp(self):
        self.address = '719%20Wisconsin%20st,Cawker%20City,KS,67430'
    
    # def test_geocode(self):
    #     the_call = ExternalApiCall()
    #     print(the_call.geocode(self.address))