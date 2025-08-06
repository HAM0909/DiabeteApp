from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib

# Initialisation de l'app FastAPI
app = FastAPI()

# Chargement des modèles .pkl au démarrage
scaler = joblib.load("model/scaler.pkl")
pca = joblib.load("model/pca_model.pkl")
kmeans = joblib.load("model/kmeans_model.pkl")

# Schéma attendu depuis le client (frontend ou appel API)
class PatientData(BaseModel):
    Pregnancies: int
    Glucose: float
    BMI: float
    Age: int
    DiabetesPedigreeFunction: float

@app.post("/predict")
def predict(data: PatientData):
    # Conversion des données en DataFrame
    input_df = pd.DataFrame([data.dict()])
    
    # 1. Scaling
    scaled = scaler.transform(input_df)

    # 2. Réduction de dimension (PCA)
    reduced = pca.transform(scaled)

    # 3. Clustering
    cluster = kmeans.predict(reduced)[0]

    # Retourne le numéro de cluster (ex : 0 ou 1)
    return {
        "cluster": int(cluster)
    }
