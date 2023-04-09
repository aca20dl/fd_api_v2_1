from typing import List
from typing import Optional
import requests
import qwikidata
import qwikidata.sparql
import time

from fastapi import Request

class Rule_Management_form:

    def __init__(self, request: Request):
        self.request: Request = request
        #self.first_time_customer = Optional[bool] = None
        #self.transaction_time = Optional[bool] = None
        #self.multiple_transactions = Optional[bool] = None
        #self.larger_purchases_avg = Optional[bool] = None
        #self.purchase_pattern = Optional[int] = None
        #self.purchase_pattern_threshold = Optional[int] = None
        #self.purchases_outside_customer_pattern = Optional[bool] = None

    async def load_data(self, request: Request):
        form = await self.request.form()
        self.first_time_customer = bool(form.get("rule1"))
        self.transaction_time = bool(form.get("rule2"))
        self.multiple_transactions = bool(form.get("rule3"))
        self.larger_purchases_avg = bool(form.get("rule4"))
        self.purchases_avg = form.get("avg_purchase")
        self.purchases_avg_threshold = form.get("avg_purchase_threshold")
        self.purchases_outside_customer_pattern = bool(form.get("rule5"))
        self.purchase_pattern = form.get("customer_pattern_threshold")
        self.matches_zip_code = bool(form.get("rule6"))
        self.is_merchant_category_prone_to_fraud = bool(form.get("rule7"))
        self.ip_matches_with_device_location_and_billing_adr = bool(form.get("rule8"))
        self.ip_address_volume = bool(form.get("rule9"))
        self.ip_address_volume_threshold = form.get("ip_volume_threshold")
        self.user_volume = bool(form.get("rule10"))
        self.user_volume_threshold = form.get("user_volume_threshold")
        self.ip_for_multiple_users = bool(form.get("rule11"))
        self.ip_for_multiple_users_threshold = form.get("ip_matches_multiple_users")
        self.ip_for_multiple_credit_cards = form.get("rule12")
        self.ip_for_multiple_credit_cards_threshold = form.get("ip_for_multiple_credit_cards_threshold")
