from fastapi import FastAPI
from app.api.v1.users.usersController import router as users_router

#register_routers FastAPI
#description: to register each router here we need to provide the router details folder name as user then register controller here
def register_routes(app:FastAPI):
    app.include_router(users_router)