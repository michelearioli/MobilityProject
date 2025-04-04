# 📍 Mobility Forecasting Project – Emilia Romagna (Italy)

## 👩‍💻 Autori
Matilde Ambrosetti (mat. 206340), Sara Galli (mat. 200831)

## 📌 Descrizione del progetto

Il progetto analizza i flussi di mobilità in Emilia-Romagna utilizzando dati forniti da TIM, basati su movimenti tra aree censuarie (ACE) tramite segnali telefonici. L'obiettivo è doppio:

- **Visualizzazione**: Creazione di mappe interattive dei flussi.
- **Modellazione predittiva**: Stima del numero di spostamenti tra zone tramite regressori ML.

## 📁 Struttura del progetto

| Cartella | Descrizione |
|---------|-------------|
| `data_analysis_and_cleansing/` | Script Python per la pulizia (`data_cleansing1.py`, `data_cleansing2.py`) e analisi dei dati aggregati (`data_analysis_province.ipynb`, `data_analysis_ACE.ipynb`). |
| `experiments_on_single_ACE/` | Esperimenti su singole aree ACE con visualizzazione e modellazione mirata. |
| `mobility_api/` | Codice per esporre il modello predittivo tramite API Flask, usando file `main.py`, `mobility_model.pkl`, `label_encoder.pkl`, `scaler.pkl`. |
| `regressions/` | Notebook per regressioni: `Regressions_layerid.ipynb`, `Regressions_toid.ipynb`, `Regressions_ACE.ipynb`, `Regressions_province.ipynb`. Include test con Random Forest, KNN, Gradient Boosting. |
| `visualization/` | Mappa interattiva della mobilità (Folium) nel file `Folium_visualization.ipynb`. Rappresentazione dei flussi in partenza/arrivo per area geografica. |
| `anaconda_projects/` | Ambiente/backup Anaconda del progetto. |
| `.virtual_documents/` | Cartella tecnica Jupyter, può essere ignorata. |

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
- Modellazione multioutput con risultati accettabili, ma influenzati dalla presenza di valori nulli in alcune categorie.

## ▶️ Esecuzione (per mobility_api)

1. Assicurarsi di avere Python ≥ 3.9.
2. Installare le dipendenze:
   ```bash
   pip install -r requirements.txt
   ```
3. Eseguire:
   ```bash
   python main.py
   ```
4. Accedere all'API su `http://localhost:5000/predict`.
