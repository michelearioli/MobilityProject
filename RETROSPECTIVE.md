# Retrospective

This repository is kept exactly as it was when I submitted my BSc thesis (July 2025), so that the code matches the thesis document. Since then I have completed most of an MSc in AI Engineering. Re-reading both the thesis and the code, I found several methodological issues and a few bugs. This file lists them openly, together with how I would address them today.

The exploratory analysis and the event-detection findings still hold up well; they were later extended into a [peer-reviewed article](https://doi.org/10.1007/s12652-026-05127-x). Most of the issues below affect the **forecasting** part.

---

## 1. Forecasting: evaluation issues

### 1.1 Random train/test split on a time series (Dozza experiments)

In the Dozza experiments (`GradientBoosting/Dozza/`), the 61 days are split into train and test sets **at random** (`train_test_split` with 10 different seeds), and the date itself is used as a numeric feature.

As a result, every test day has neighbouring days in the training set, and the model mostly *interpolates* between them instead of forecasting. The lag features make this worse: `lag_1` of a test day is the target of a training day. The reported MAPE of about 8% is therefore optimistic, and it does not measure the ability to predict *future* days.

**Today:** I would use a chronological split or a rolling-origin evaluation (`TimeSeriesSplit`), always training on the past and testing on the future.

### 1.2 The date as a feature cannot extrapolate

The date is encoded as a nanosecond timestamp and fed to a tree ensemble. Trees cannot extrapolate: any date after the training period falls into the same leaves as the last training days.

This is easy to see by querying the deployed model for Dozza:

| Requested date | Prediction |
|---|---|
| Tue 2019-09-10 (inside the data) | 10,195 |
| Tue 2025-06-03 | 10,520 |
| Tue 2030-01-01 | 10,520 |

Predictions for any future date are essentially the same value. The `week` feature also breaks outside August–September: it is computed as `isocalendar().week - 35`, so January dates get negative weeks.

**Today:** I would drop the absolute date and keep only features that recur over time: weekday, holiday calendar, and lags of the target.

### 1.3 No baseline

The models are never compared with a trivial forecaster, such as a *seasonal naive* model ("same as the same weekday last week") or a per-ACE weekday average. Without a baseline it is impossible to tell how much Gradient Boosting actually adds.

**Today:** I would report every result next to a seasonal-naive baseline, and use MASE alongside MAPE.

### 1.4 Too little data for stable metrics

With 61 days, a 30% test set is about 18–20 days. In the Dozza experiments the MAPE changes from 7.4% to 10.3% depending only on the random seed, and from 7.6% to 16.3% in the full-dataset variant. Single-number results hide this variance.

**Today:** I would report mean ± standard deviation across folds, and treat feature-set differences smaller than that spread as inconclusive.

### 1.5 MAPE on small flows

MAPE explodes when the true value is small. In the generalization experiment, a few low-traffic ACEs have MAPE above 50%, up to 104%, and they dominate the average.

**Today:** I would add MAE, WAPE (total absolute error divided by total volume) or MASE, which do not depend on the scale of each ACE.

---

## 2. Forecasting: bugs in the generalization experiment

### 2.1 Lag features computed across ACEs

In `GradientBoosting/Generalization/BestFeature_all.ipynb` the lags are computed as:

```python
df[f'lag_{lag}'] = df['datavalue'].shift(lag)
```

The dataframe contains all ACEs sorted by date, so `shift(1)` returns the flow of **another ACE on the same day**, not the flow of the same ACE on the previous day. The "lag" feature set (set3) is therefore not what it was meant to be.

**Fix:**

```python
df = df.sort_values(['toid', 'date'])
df[f'lag_{lag}'] = df.groupby('toid')['datavalue'].shift(lag)
```

Missing values should also not be filled with 0: that tells the model "zero people arrived". The first days should be dropped instead.

### 2.2 The code and the thesis disagree

- The thesis describes the generalization as **one model per ACE** (61 rows each). The notebook trains **one global model** on all ACEs, with the ACE id as a feature.
- The thesis reports mean MAPEs of 12.08% (set1), 12.47% (set2) and **9.92% (set3, lags)**. The output saved in the notebook gives 10.4% (set1), 10.8% (set2) and **15.7% (set3)**. This is consistent with the lag bug above.

Because of 2.1, the conclusion in the thesis that "lag features generalize best" is not supported by the code in this repository.

---

## 3. Event detection

The Z-score method found real events, such as Cersaie at the Bologna fair district, motorsport events at Imola and Festivalfilosofia in Modena. It also has clear limitations:

- **Global baseline.** The mean and standard deviation are computed over the whole two months. They ignore the daily and weekly cycle, so a normal Monday morning and a quiet Sunday night are compared with the same reference.
- **Non-robust statistics.** The events themselves inflate the mean and the standard deviation, which partly masks them.
- **Hours with zero flow are dropped** before computing the statistics, which shifts the baseline.

**Today:** I would compare each hour only with the same hour on the same weekday (a context-aware baseline, as the journal article suggests). I would use the median and the MAD instead of the mean and standard deviation, or apply STL decomposition and run detection on the residuals.

---

## 4. Engineering

- **The deployed model does not match its notebook.** The saved `scaler.pkl` was fitted on a column named `layerid`, the ACE of *origin*. The notebook in `mobility_api/model/` builds the features from `toid`, the ACE of *destination*. The pickle was produced by a different version of the code, so it is unclear whether the API predicts arrivals (as documented) or departures.
- **No reproducibility.** The packages in `requirements.txt` have no fixed versions. The pickles only load with scikit-learn 1.6.x; newer versions fail on them. The API split also uses no `random_state`.
- **Error handling in the API.** On a failure, `/predict` returns HTTP 200 with an `error` field, instead of a 4xx or 5xx status code.
- **Slow ingestion.** `data_cleansing2.py` inserts and commits ~36M rows one at a time. A bulk `COPY` or batched inserts would be orders of magnitude faster. Records discarded by the checks are only printed, never counted or logged.
- **Notebooks as the only code.** Feature engineering is copy-pasted across notebooks with small differences, which is how the bugs above went unnoticed. Today I would move it into a shared, tested Python module.

---

## What I learned

The biggest lesson was that **the evaluation setup matters more than the model**. A random split and a feature that leaks the future produced numbers that looked excellent and meant little. Today I would start a forecasting project by fixing the split, the baseline and the metric, and only then choose the model.
