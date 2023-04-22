from typing import List
from typing import Optional
from random import randint

import requests
from fastapi import Request, Form
from requests.structures import CaseInsensitiveDict


class UserCreateForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.company_id: Optional[str] = None
        self.company_name: Optional[str] = None
        self.email:Optional[str] = None
        self.password: Optional[str] = None
        self.company_category: Optional[str] = None
        self.merch_lat: Optional[str] = None
        self.merch_long: Optional[str] = None


    async def load_data(self):



        print("debug1")
        form = await self.request.form()
        country = form.get("country")
        print(country)
        zip = form.get("zip").lower()
        location_details = self.get_location_details(zip, country)
        self.company_id = randint(1000, 9999)
        self.company_name = form.get("company_name")
        self.email = form.get("email")
        self.password = form.get("password")
        self.company_category = form.get("categories")
        self.merch_lat = location_details['features'][0]['properties']['lat']
        self.merch_long = location_details['features'][0]['properties']['lon']

    async def is_valid(self):
        if not self.company_name:
            self.errors.append("Company Name is required")
        if not self.email or not (self.email.__contains__("@")):
            self.errors.append("Email is required")
        if not self.password or not (len(self.password) >= 8):
            self.errors.append("Password must be of at least length 8")
        if not self.errors:
            return True
        return False

    import requests
    from requests.structures import CaseInsensitiveDict

    def country_name_to_code(self, country_name):
        url = f"https://restcountries.com/v3.1/name/{country_name}"
        response = requests.get(url)

        if response.status_code == 404:
            raise ValueError(f"Country name '{country_name}' not found")
        elif response.status_code != 200:
            raise Exception(f"API request failed with status code {response.status_code}")

        country_data = response.json()
        country_code = country_data[0]['cca2']

        return country_code

    def get_location_details(self, postcode, country):
        country_code = self.country_name_to_code(country).lower()
        api_key = "a5f3370f6b6442f8803b7e4a6900dfa6"
        url = f"https://api.geoapify.com/v1/geocode/search?text={postcode}&lang=en&limit=10&type=postcode&filter=countrycode:{country_code}&apiKey={api_key}"

        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"

        resp = requests.get(url, headers=headers)
        location_details = resp.json()
        return location_details



