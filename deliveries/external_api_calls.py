import json
import requests
import environ

# Initialise environment variables
env = environ.Env()
environ.Env.read_env()


class ExternalApiCall:

    def geocode(self, address):

            key = env('GOOGLE_KEY')
            geo_code_base_url = 'https://maps.googleapis.com/maps/api/geocode/json?address='
            url = geo_code_base_url + address + key
            res = requests.get(url)
            data = res.json()
            print(res)
            # return data