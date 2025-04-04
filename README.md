# 📍 Mobility Forecasting Project – Emilia Romagna (Italy)

## 📌 Descrizione del progetto

Il progetto analizza i flussi di mobilità in Emilia-Romagna utilizzando dati forniti da TIM, basati su movimenti tra aree censuarie (ACE) tramite segnali telefonici. L'obiettivo è doppio:

- **Visualizzazione**: Creazione di mappe interattive dei flussi.
- **Modellazione predittiva**: Stima del numero di spostamenti tra zone tramite regressori ML.

## 📁 Struttura del progetto

| Cartella | Descrizione |
|---------|-------------|
| `data_analysis_and_cleansing/` | Script Python per la pulizia e caricamento su PostgreSQL (`data_cleansing1.py`, `data_cleansing2.py`) e analisi dei dati aggregati (`data_analysis_province.ipynb`, `data_analysis_ACE.ipynb`). |
| `experiments_on_single_ACE/` | Analisi dettagliata su singole aree ACE. Contiene: <br>• `ACE_in-out.ipynb`: analisi degli spostamenti in entrata/uscita da un singolo ACE. <br>• `ACE_in-out_CATEGORIES.ipynb`: analisi con suddivisione demografica (età, sesso, ecc). <br>• `Dozza_Analisys/`: approfondimento sull’area di Dozza con analisi specifiche. |
| `mobility_api/` | API sviluppata con **FastAPI** per esporre il modello predittivo. Contiene: <br>• `main.py`: definizione dell'endpoint `/predict` che riceve `date` e `layerid` e restituisce la previsione. <br>• `mobility_model.pkl`, `label_encoder.pkl`, `scaler.pkl`: oggetti salvati del modello e preprocessori. <br>• `requirements.txt`: librerie richieste per l’esecuzione dell’API. |
| `regressions/` | Notebook per regressioni: `Regressions_layerid.ipynb` (numero di persone che lasciano un ACE in una certa data), `Regressions_toid.ipynb` (numero di persone che entrano in un ACE in una certa data), `Regressions_ACE.ipynb` (numero di persone che lasciano un ACE per entrare in un altro ACE), `Regressions_province.ipynb` (numero di persone che lasciano una provincia per entare in un altra provincia). Include test con Random Forest, KNN, Gradient Boosting. |
| `visualization/` | Mappa interattiva della mobilità (Folium) nel file `Folium_visualization.ipynb`. Rappresentazione dei flussi in partenza/arrivo per area geografica. Strumento per visualizzazione singolo ACE nel file `ACE_visualization.ipynb`. |

## 🧪 Dataset

- **Fonte**: TIM Enterprise – dati agosto/settembre 2019.
- **Contenuti**: Spostamenti tra aree (layerid → toid), dati demografici, motivi di spostamento, coordinate GeoJSON.
- **Importazione**: I CSV vengono puliti e caricati su database PostgreSQL.

## 📊 Modelli e Tecniche

- **Modelli usati**: Random Forest, K-Nearest Neighbors (KNN), Gradient Boosting.
- **Feature**: Data, giorno della settimana, weekend, etc.
- **Valutazione**: MAE, MAPE.
- **Output multi-target**: Previsioni su sesso, età, nazionalità e motivo dello spostamento.

## 📌 Risultati principali

- Gradient Boosting ha fornito i migliori risultati in termini di MAPE.
- Visualizzazione efficace tramite Folium.

## ▶️ Esecuzione dell'API (`mobility_api`)

1. Assicurarsi di avere Python ≥ 3.9 installato.
2. Installare le dipendenze:
   ```bash
   pip install -r requirements.txt
   ```
3. Avviare il server con uvicorn:
   ```bash
   uvicorn main:app --reload
   ```
4. Accedere alla documentazione interattiva:
   - Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
   - ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)
5. Endpoint disponibile:
   ```
   POST /predict
   Body JSON:
   {
     "date": "YYYY-MM-DD",
     "layerid": "ACE_ID"
   }
   ```

