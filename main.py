# main.py
""" #####################################################################
Created by: Anshul Pareek
Modified by: Anshul pAREEK
Last Modified Date: 20Apr25

Purpose: Its the main file or root file from where all code will run
usage: once setup the virtual env then run 

COMMAND: uvicorn main:app --reload 
######################################################################"""
from fastapi import FastAPI
from app.database.mysqlConnection import engine
from app.entities import user, company
from fastapi import FastAPI
#from app.routers import register_routes
import importlib
import pkgutil
from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from app.utils.responseHandler import http_exception_handler, validation_exception_handler

app = FastAPI()
user.Base.metadata.create_all(bind=engine)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

#register_routes(app)
def include_all_routers(app, package):
    # Discover all modules under the given package
    package_path = package.__path__
    package_name = package.__name__

    for _, module_name, _ in pkgutil.iter_modules(package_path):
        module = importlib.import_module(f"{package_name}.{module_name}.{module_name}Controller")
        router = getattr(module, "router", None)
        if router:
            app.include_router(router)

# Import your versioned api package
import app.api.v1 as v1

# Dynamically include all routers
include_all_routers(app, v1)