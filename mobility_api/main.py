from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Literal

# Caricamento del modello, dello scaler e dell'encoder salvati
try:
    model = joblib.load("mobility_model.pkl")
    scaler = joblib.load("scaler.pkl")
    label_encoder = joblib.load("label_encoder.pkl")
    print("Modello, scaler e encoder caricati correttamente.")
except Exception as e:
    print("Errore nel caricamento del modello o dei preprocessori:", e)

# Definizione del formato dei dati in input
class MobilityRequest(BaseModel):
    date: str  # formato: 'YYYY-MM-DD'
    layerid: str  # ID geografico ACE come stringa

# Istanza dell'app FastAPI
app = FastAPI()


@app.post("/predict")
def predict_mobility(req: MobilityRequest):
    try:
        # Conversione della data in datetime
        date_obj = datetime.strptime(req.date, "%Y-%m-%d")

        # Creazione delle feature derivate
        weekday = date_obj.weekday()
        week = date_obj.isocalendar().week - 35  # adatta il min come nel training (es: week.min = 35)
        weekend = 1 if weekday in [5, 6] else 0
        date_int = int(date_obj.timestamp() * 1e9)  # int64 formato timestamp simile a quello nel dataset

        # Encoding layerid come fatto nel training
        encoded_layerid = label_encoder.transform([req.layerid])[0]

        # Creazione del DataFrame in input con tutte le feature originali
        X = pd.DataFrame([{
            "date": date_int,
            "layerid": encoded_layerid,
            "weekday": weekday,
            "week": week,
            "weekend": weekend
        }])

        print("Input ricevuto:", X)

        # Scaling
        X_scaled = scaler.transform(X)

        # Predizione logaritmica
        y_log_pred = model.predict(X_scaled)

        # Inverso del log1p usato nel training
        y_pred = np.expm1(y_log_pred)

        print("Predizione completata:", y_pred)

        return {"prediction": float(y_pred[0])}

    except Exception as e:
        print("Errore durante la predizione:", e)
        return {"error": str(e)}
