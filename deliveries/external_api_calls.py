import json
import requests
import environ

import googlemaps


# Initialise environment variables
env = environ.Env()
environ.Env.read_env()

class GoogleCalls:

    def __init__(self) -> None:
        self.gmaps = googlemaps.Client(key=env('GOOGLE_KEY'))

    def get_location_info(self, location):

        place_id = self.gmaps.find_place(location, 'textquery')['candidates']

        if len(place_id) > 0 :
            place_id = place_id[0]['place_id']

            location_info = self.gmaps.place(place_id)['result']
            if 'business_status' in location_info:
                if location_info['business_status'] == 'OPERATIONAL':
                    return {'status': {'request_status': 'valid',
                            'business_status':location_info['business_status']
                            }, 
                            'hours': location_info['opening_hours']['weekday_text'], 
                            'latitude' : location_info['geometry']['location']['lat'],
                            'longitude' : location_info['geometry']['location']['lng'],
                            'name' : location_info['name'],
                            'phone' : location_info['formatted_phone_number'],} 
                else:
                    return {'status' : {'request_status': 'valid',
                            'business_status':location_info['business_status']
                            }}
            else:
                return {'status':{'request_status': 'no request results',
                                'business_status' : 'no business results'}}
        else:
            return {'status':{'request_status': 'no request results',
                            'business_status' : 'no business results'}}

    def format_location(self, data):
        return f"{data['name']}, {data['street']}, {'Suite' + data['suite'] + ', ' if data['suite'] else ''}{data['city']}, {data['state']}, {data['postal_code']}"

    def places(self, data):

        formatted_location = self.format_location(data)
        return self.get_location_info(formatted_location)