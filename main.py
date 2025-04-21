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
from app.entities import user
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Depends, status
from typing import Annotated
from sqlalchemy.orm import Session
from app.routers import register_routes

app = FastAPI()
user.Base.metadata.create_all(bind=engine)
register_routes(app)

