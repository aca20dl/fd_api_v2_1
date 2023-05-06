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
        self.age1 = form.get("age1")
        self.age2 = form.get("age2")
        self.age3 = form.get("age3")
        self.age4 = form.get("age4")
        self.age5 = form.get("age5")
        self.age6 = form.get("age6")
        self.f_age1 = form.get("f_age1")
        self.f_age2 = form.get("f_age2")
        self.f_age3 = form.get("f_age3")
        self.f_age4 = form.get("f_age4")
        self.f_age5 = form.get("f_age5")
        self.f_age6 = form.get("f_age6")
        self.time_threshold_m_t = form.get("time_threshold_m_t")
        self.num_multiple_transactions_threshold = form.get("num_multiple_transactions_threshold")
        self.first_time_customer = bool(form.get("rule1"))
        self.transaction_time = bool(form.get("rule2"))
        self.multiple_transactions = bool(form.get("rule3"))
        self.larger_purchases_avg = bool(form.get("rule4"))
        self.purchases_avg = form.get("avg_purchase")
        self.purchases_avg_threshold = form.get("avg_purchase_threshold")
        self.purchases_outside_customer_time_frame = bool(form.get("rule5"))
        self.purchase_pattern = form.get("customer_pattern_threshold")
        self.matches_zip_code = bool(form.get("rule6"))
        self.is_merchant_category_prone_to_fraud = bool(form.get("rule7"))
        self.merchant_category = form.get("company_category")
        self.ip_matches_with_device_location_and_billing_adr = bool(form.get("rule8"))
        self.ip_address_volume = bool(form.get("rule9"))
        self.ip_address_volume_threshold = form.get("ip_volume_threshold")
        self.transaction_time_customer_pattern = bool(form.get("rule10"))
        self.user_volume_threshold = form.get("user_volume_threshold")
        self.ip_for_multiple_users = bool(form.get("rule11"))
        self.ip_for_multiple_users_threshold = form.get("ip_matches_multiple_users")
        self.ip_for_multiple_credit_cards = bool(form.get("rule12"))
        self.ip_for_multiple_credit_cards_threshold = form.get("ip_for_multiple_credit_cards_threshold")
        self.location_for_multiple_credit_cards = bool(form.get("rule14"))
        self.device_transaction_volume = form.get("rule13")
        self.merch_location_customer_location_distance = bool(form.get("rule15"))
        self.merch_location_customer_location_distance_threshold = form.get("merch_location_customer_location_distance_threshold")
        self.time_threshold = form.get("time_threshold")
        self.distance_threshold = form.get("distance_threshold")
        self.same_credit_card_different_location_short_time = bool(form.get("rule16"))
