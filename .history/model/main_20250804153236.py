from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from database import sessionLocal
from models import Base, engine, Patient, Prediction
import pandas as pd
import joblib
import datetime
impo
