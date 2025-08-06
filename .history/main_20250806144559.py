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
scaler = joblib.load("model/scaler.pkl")
pca_model = joblib.load("model/pca_model.pkl")

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("add_patient.html", {"request": request, "result": None})

@app.post("/submit", response_class=HTMLResponse)
def submit(
    request: Request,
    name: str = Form(...),
    pregnancies: int = Form(...),
    glucose: float = Form(...),
    bmi: float = Form(...),
    age: int = Form(...),
    diabetes_pedigree: float = Form(...)
):
    df = pd.DataFrame([{
        "Pregnancies": pregnancies,
        "Glucose": glucose,
        "BMI": bmi,
        "age": age,
        "DiabetesPedigreeFunction": diabetes_pedigree
    }])

    scaled = 