# BikeShare | Next-day demand forecasting

Public dataset: [UCI Bike Sharing Dataset](https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset) (Fanaee-T, 2013), licensed CC BY 4.0. Daily records from 2011–2012, 731 dates.

**Reproducible model experiment:** Train a next-day forecaster from lagged daily rentals, calendar seasonality, and pre-known holidays. Avoid current-day rentals, future demand, and actual same-day weather. Validate on 120 historical days and evaluate on a later 120-day holdout.

**Prior local evaluation** (re-run to verify on your machine): Ridge regression, MAE 919.94 rentals/day versus last-week benchmark MAE 1342.27 (31.46% lower). This is a *one-day-ahead walk-forward backtest using known past observations*, not a 120-day advance prediction or a currently deployed service.

Download official `day.csv` from UCI, place it in this folder, then run:

```bash
python -m pip install -r requirements.txt
python train.py --csv day.csv
```

Source code reports baseline and holdout MAEs. Dataset is *not* Apex Pack data. Never upload private operational records here.

Limitations: dated research dataset, no weather forecast or real-time decision integration; holiday/calendar data assumed known at forecast time.