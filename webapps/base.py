from webapps.transactions import route_transactions
from fastapi import APIRouter
from webapps.users import route_users
from webapps.auth import route_login


api_router = APIRouter()
api_router.include_router(route_transactions.router, prefix="", tags=["transaction-webapp"])
api_router.include_router(route_users.router, prefix="", tags=["users-webapp"])
api_router.include_router(route_login.router, prefix="", tags=["auth-webapp"])
