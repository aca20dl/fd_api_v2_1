from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from apis.general_pages.route_homepage import general_pages_router
from core.config import Settings
from db.session import engine
from db.base import Base


#   OLD -----       app = FastAPI(title="FraudDetector", version="0.0.1")

#        OLD --------     app.include_router(user_router.router)

templates = Jinja2Templates(directory="Templates")


def include_router(app):
    app.include_router(general_pages_router)


def configure_static(app):
    app.mount('/static', StaticFiles(directory='static'), name='static')

def create_tables():
    print("create_tables")
    Base.metadata.create_all(bind=engine)


def start_application():
    app = FastAPI(title=Settings.PROJECT_NAME, version=Settings.PROJECT_VERSION)
    include_router(app)
    configure_static(app)
    create_tables()
    return app





app = start_application()

# @app.get("/")
# def home(request: Request):
#
#   return templates.TemplateResponse("home.html" , {
#        "request": request
#    })
# @app.get("/login")
# def login(request: Request):
#    login = 'login'
#    return templates.TemplateResponse("login.html" , {
#        "request": request, 'login': login
#    })
#
# @app.get("/register")
# def register(request: Request):
#    register = 'register'
#    return templates.TemplateResponse("register.html", {
#        "request": request, 'register': register
#    })
