from typing import List
from typing import Optional
from random import randint


from fastapi import Request, Form


class UserCreateForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.company_id: Optional[str] = None
        self.company_name: Optional[str] = None
        self.email:Optional[str] = None
        self.password: Optional[str] = None
        self.company_category: Optional[str] = None

        async def load_data(self):
            print("debug1")
            form = await self.request.form()
            self.company_id = randint(1000, 9999)
            self.company_name = form.get("company_name")
            self.email = form.get("email")
            self.password = form.get("password")
            self.company_category = form.get("company_category")

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



