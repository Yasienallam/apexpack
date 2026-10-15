"""Public UCI bike sharing: leakage-conscious one-day-ahead evaluation."""
import argparse
import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_absolute_error

def run(path):
    raw = pd.read_csv(path)
    required = {"dteday", "cnt", "holiday"}
    if not required.issubset(raw.columns):
        raise ValueError(f"Required columns missing: {required-set(raw.columns)}")
    d = raw.loc[:, ["dteday", "cnt", "holiday"]].copy()
    d["date"] = pd.to_datetime(d.pop("dteday"))
    d = d.sort_values("date").reset_index(drop=True)
    if d["date"].duplicated().any() or d[["date","cnt","holiday"]].isna().any().any():
        raise ValueError("Missing values / duplicate dates")
    d["trend"] = np.arange(len(d))
    d["day_of_week"] = d["date"].dt.dayofweek
    d["is_weekend"] = (d["day_of_week"]>=5).astype(int)
    d["month"] = d["date"].dt.month
    angle = 2*np.pi*(d["date"].dt.dayofyear - 1)/365.25
    d["sin_doy"], d["cos_doy"] = np.sin(angle), np.cos(angle)
    for lag in [1,7,14,28]:
        d[f"lag_{lag}"] = d["cnt"].shift(lag)
    for days in [7,28]:
        d[f"mean_{days}"] = d["cnt"].shift(1).rolling(days).mean()
    d["std_7"] = d["cnt"].shift(1).rolling(7).std()
    features = ["trend","day_of_week","is_weekend","month","holiday","sin_doy","cos_doy",
                "lag_1","lag_7","lag_14","lag_28","mean_7","mean_28","std_7"]
    d = d.dropna(subset=features).reset_index(drop=True)
    if len(d)<450:
        raise ValueError("Not enough data for chronological train/validation/test")
    train, validation, test = d.iloc[:-240], d.iloc[-240:-120], d.iloc[-120:]
    baselines = {"Yesterday": "lag_1", "Last week": "lag_7", "Last 7 days": "mean_7"}
    trials = {k: mean_absolute_error(validation["cnt"], validation[v])
              for k,v in baselines.items()}
    model = make_pipeline(StandardScaler(), Ridge(alpha=25))
    model.fit(train[features], train["cnt"])
    trials["Ridge"] = mean_absolute_error(validation["cnt"], np.clip(model.predict(validation[features]),0,None))
    winner = min(trials, key=trials.get)
    if winner == "Ridge":
        model.fit(pd.concat([train,validation])[features], pd.concat([train,validation])["cnt"])
        pred = np.clip(model.predict(test[features]),0,None)
    else:
        pred = test[baselines[winner]]
    actual = test["cnt"]
    test_mae = mean_absolute_error(actual,pred)
    benchmark_mae = mean_absolute_error(actual,test["lag_7"])
    print(f"Train {len(train)}; validation {len(validation)}; test {len(test)}")
    print("Validation MAE:", {k:round(v,2) for k,v in trials.items()})
    print(f"Selected from validation: {winner}")
    print(f"Holdout MAE: {test_mae:.2f}; last-week MAE: {benchmark_mae:.2f}")
    print(f"MAE reduction vs last week: {(benchmark_mae-test_mae)/benchmark_mae*100:.2f}%")
    print("Method: 1-day-ahead historical backtest with observed prior-day rental counts.")

if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--csv",default="day.csv")
    run(parser.parse_args().csv)
