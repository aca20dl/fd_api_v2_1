from datetime import datetime
from typing import List
from typing import Optional
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
        self.merchant: Optional[str] = None
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
        self.merchant_latitude: Optional[str] = None
        self.merchant_longitude: Optional[str] = None
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
        self.first_name = form.get("first_name")
        self.surname = form.get("surname")
        self.gender = form.get("gender")
        self.dob = form.get("dob")
        self.merchant = form.get("merchant")
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
        self.unix_time = int(time.time())
        self.date_and_time = str(datetime.fromtimestamp(time.time()))
        self.merchant_latitude = location_details["latitude"]
        self.merchant_longitude = location_details["longitude"]
        self.is_fraud = 2

    def getGeoLocation(self, request: Request):
        #ip = request.client.host
        ip = "8.8.8.8"
        url = f"https://ipapi.co/{ip}/json"

        r = requests.get(url)

        location_details = r.json()

        return location_details

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