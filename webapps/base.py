from webapps.transactions import route_transactions, route_create_transactions
from fastapi import APIRouter
from webapps.users import route_users
from webapps.auth import route_login
from webapps.fraud_detector.rule_based import route_rb_fd
from webapps.home import home_router


api_router = APIRouter()
api_router.include_router(route_transactions.router, prefix="", tags=["transaction-webapp"])
api_router.include_router(route_users.router, prefix="", tags=["users-webapp"])
api_router.include_router(route_login.router, prefix="", tags=["auth-webapp"])
api_router.include_router(route_create_transactions.router, prefix="", tags=["transaction-create-webapp"])
api_router.include_router(route_rb_fd.router, prefix="", tags=["rb_fd_system"])
api_router.include_router(route_rb_fd.router, prefix="", tags=["rule_form"])
api_router.include_router(home_router.router, prefix="", tags=["home"])