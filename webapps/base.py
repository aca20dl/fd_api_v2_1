from webapps.transactions import route_transactions
from fastapi import APIRouter
from webapps.users import route_users


api_router = APIRouter()
api_router.include_router(route_transactions.router, prefix="", tags=["transaction-webapp"])
api_router.include_router(route_users.router, prefix="", tags=["users-webapp"])
