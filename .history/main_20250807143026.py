from fastapi import FastAPI, Request, Form
from contextlib import asynccontextmanager
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from database import async_session, Base, engine
from sqlalchemy.ext.asyncio import AsyncSession
from models import Patient, Prediction
import pandas as pd
import joblib
import datetime
import os


app = FastAPI()

templates = Jinja2Templates(directory="templates")


kmeans = joblib.load("model/kmeans_model.pkl")
scaler = joblib.load("model/scaler.pkl")
pca_model = joblib.load("model/pca_model.pkl")

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn run_sync(Base.metadata.create_all):
    yield


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("add_patient.html", {"request": request, "result": None})

@app.post("/submit", response_class=HTMLResponse)
async def submit(
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

    scaled = scaler.transform(df)
    reduced = pca_model.transform(scaled)
    prediction = kmeans.predict(reduced) [0]

    result_text = "Diabétique" if prediction == 1 else "Non diabétique"


    db = sessionLocal()


    new_patient = Patient(
        name=name,
        age=age,
        glucose=glucose,
        bmi=bmi,
        pregnancies=pregnancies,
        pedigree=diabetes_pedigree,
        resultat=prediction,
        created_at=datetime.datetime.now()

    )

    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    new_prediction = Prediction(
        patientid=new_patient.id,
        result=prediction,
        created_at=datetime.datetime.now()
    )

    db.add(new_prediction)
    db.commit()
    db.close()


    return templates.TemplateResponse("add_patient.html",{
        "request": request,
        "result": result_text
    })



