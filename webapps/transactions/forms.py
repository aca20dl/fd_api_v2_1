import socket
from datetime import datetime
from typing import List
from typing import Optional

import psutil
import requests
import qwikidata
import qwikidata.sparql
import time



from fastapi import Request




class TransactionCreateForm:

    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.first_name: Optional[str] = None
        self.surname: Optional[str] = None
        self.gender: Optional[str] = None
        self.dob: Optional[str] = None
        self.merchant_category: Optional[str] = None
        self.cc_number: Optional[str] = None
        self.amount: Optional[float] = None
        self.state: Optional[str] = None
        self.city: Optional[str] = None
        self.zip: Optional[str] = None
        self.city_population: Optional[int] = None
        self.job: Optional[str] = None
        self.transaction_number: Optional[str] = None
        self.latitude: Optional[str] = None
        self.longitude: Optional[str] = None
        self.unix_time: Optional[str] = None
        self.date_and_time: Optional[int] = None
        self.device_latitude: Optional[str] = None
        self.device_longitude: Optional[str] = None
        self.merchant_id: Optional[str] = None
        self.ip_address: Optional[str] = None
        self.is_fraud: Optional[bool] = None


    async def load_data(self, request: Request):
        form = await self.request.form()
        location_details = self.getGeoLocation(request)
        print(location_details)
        city_x = location_details['city']
        country_x = location_details['country_name']
        print(city_x)
        print(country_x)
        population_details = self.getCityDetails(city_x, country_x)
        form = await self.request.form()
        self.merchant_id = form.get("merchant")
        self.first_name = form.get("first_name")
        self.surname = form.get("surname")
        self.gender = form.get("gender")
        self.dob = form.get("dob")
        self.merchant_category = form.get("merchant_category")
        self.cc_number = form.get("cc_number")
        self.amount = form.get("amount")
        self.state = form.get("state")
        self.city = form.get("city")
        self.street = form.get("street")
        self.zip = form.get("zip")
        print(population_details)
        self.city_population = population_details['population']['value']
        self.job = form.get("job")
        self.transaction_number = 1
        self.latitude = location_details["latitude"]
        self.longitude = location_details["longitude"]
        date = form.get('date')
        time_x = form.get('time')
        self.date_and_time = date + ' ' + time_x
        datetime_obj = datetime.strptime(self.date_and_time, '%Y-%m-%d %H:%M:%S.%f')
        self.unix_time = int(time.mktime(datetime_obj.timetuple()))
        self.device_latitude = form.get("device_latitude")
        self.device_longitude = form.get("device_longitude")
        self.ip_address = (self.get_inet_ip_address('wlp1s0'))
        self.is_fraud = 2

    def getGeoLocation(self, request: Request):
        url = "https://ipapi.co/json/?key=wGlBET16UoZx73OkmJhv9X2gT9JDPsMyQyj1QclYc2FYkCwuaX"

        r = requests.get(url)
        print(r.text)

        if r.status_code == 200:
            location_details = r.json()
        else:
            print("Request failed with status code:", r.status_code)

        return location_details

    # This function
    def getCityDetails(self, city, country):
        query = """
            SELECT ?city ?cityLabel ?country ?countryLabel ?population
            WHERE
            {
              ?city rdfs:label '%s'@en.
              ?city wdt:P1082 ?population.
              ?city wdt:P17 ?country.
              ?city rdfs:label ?cityLabel.
              ?country rdfs:label ?countryLabel.
              FILTER(LANG(?cityLabel) = "en").
              FILTER(LANG(?countryLabel) = "en").
              FILTER(CONTAINS(?countryLabel, "%s")).
            }
            """ % (city, country)

        res = qwikidata.sparql.return_sparql_query_results(query)
        out = res['results']['bindings'][0]
        return out


    # This function's goal is to retrieve the IP address of the network
    def get_inet_ip_address(self, interface_name=None):
        for interface, addrs in psutil.net_if_addrs().items():
            if interface_name is None or interface == interface_name:
                for addr in addrs:
                    if addr.family == socket.AF_INET:
                        return addr.address
        return None

