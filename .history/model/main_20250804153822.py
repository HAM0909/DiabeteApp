from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from database import sessionLocal
from models import Base, engine, Patient, Prediction
import pandas as pd
import joblib
import datetime
import os


app = FastAPI()
templates = Jinja2Templates(directory="templates")

Base.metadata.create_all(bind=engine)

kmeans = joblib.load("model/kmeans_model.pkl")
sca
