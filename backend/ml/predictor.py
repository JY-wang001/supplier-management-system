import pandas as pd
import numpy as np
from datetime import date, timedelta
from sqlalchemy.orm import Session
from models.supplier import PriceHistory, WeatherData
from typing import List, Dict


class SimpleLinearRegression:
    def __init__(self):
        self.coef_ = None
        self.intercept_ = None

    def fit(self, X, y):
        n = len(y)
        X = np.array(X)
        y = np.array(y)

        if X.ndim == 1:
            X = X.reshape(-1, 1)

        X_b = np.c_[np.ones((n, 1)), X]
        theta = np.linalg.inv(X_b.T.dot(X_b)).dot(X_b.T).dot(y)

        self.intercept_ = theta[0]
        self.coef_ = theta[1:]

        return self

    def predict(self, X):
        X = np.array(X)
        if X.ndim == 1:
            X = X.reshape(-1, 1)
        X_b = np.c_[np.ones((len(X), 1)), X]
        return X_b.dot(np.r_[self.intercept_, self.coef_])


def mean_squared_error(y_true, y_pred):
    return np.mean((np.array(y_true) - np.array(y_pred)) ** 2)


def r2_score(y_true, y_pred):
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    ss_total = np.sum((y_true - np.mean(y_true)) ** 2)
    ss_residual = np.sum((y_true - y_pred) ** 2)
    return 1 - (ss_residual / ss_total)


def prepare_data(db: Session, supplier_id: int, product_name: str):
    price_history = db.query(PriceHistory).filter(
        PriceHistory.supplier_id == supplier_id,
        PriceHistory.product_name == product_name
    ).order_by(PriceHistory.date).all()

    if len(price_history) < 10:
        return None, None

    dates = []
    prices = []
    temperatures = []
    humidities = []
    precipitations = []

    for record in price_history:
        dates.append(record.date)
        prices.append(record.price)

        weather = db.query(WeatherData).filter(
            WeatherData.date == record.date
        ).first()

        if weather:
            temperatures.append(weather.temperature)
            humidities.append(weather.humidity)
            precipitations.append(weather.precipitation)
        else:
            temperatures.append(np.nan)
            humidities.append(np.nan)
            precipitations.append(np.nan)

    df = pd.DataFrame({
        'date': dates,
        'price': prices,
        'temperature': temperatures,
        'humidity': humidities,
        'precipitation': precipitations
    })

    df = df.dropna()
    df['date_ordinal'] = df['date'].apply(pd.Timestamp.toordinal)

    X = df[['date_ordinal', 'temperature', 'humidity', 'precipitation']].values
    y = df['price'].values

    return X, y


def train_model(X, y):
    n_samples = len(y)
    test_size = int(n_samples * 0.2)
    indices = np.random.permutation(n_samples)
    train_indices, test_indices = indices[test_size:], indices[:test_size]

    X_train, X_test = X[train_indices], X[test_indices]
    y_train, y_test = y[train_indices], y[test_indices]

    model = SimpleLinearRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    return model, {'mse': mse, 'r2': r2}


def predict_prices(db: Session, supplier_id: int, product_name: str, days_ahead: int = 7) -> Dict:
    X, y = prepare_data(db, supplier_id, product_name)

    if X is None:
        return {
            'predictions': [],
            'model_metrics': {'error': 'Insufficient data for prediction'}
        }

    model, metrics = train_model(X, y)

    last_date = db.query(PriceHistory.date).filter(
        PriceHistory.supplier_id == supplier_id,
        PriceHistory.product_name == product_name
    ).order_by(PriceHistory.date.desc()).first()[0]

    predictions = []
    for i in range(1, days_ahead + 1):
        prediction_date = last_date + timedelta(days=i)

        weather = db.query(WeatherData).filter(
            WeatherData.date == prediction_date
        ).first()

        if weather:
            temp = weather.temperature
            humidity = weather.humidity
            precipitation = weather.precipitation
        else:
            temp = np.mean(X[:, 1])
            humidity = np.mean(X[:, 2])
            precipitation = np.mean(X[:, 3])

        date_ordinal = pd.Timestamp(prediction_date).toordinal()
        features = np.array([[date_ordinal, temp, humidity, precipitation]])
        predicted_price = model.predict(features)[0]

        predictions.append({
            'date': prediction_date.strftime('%Y-%m-%d'),
            'predicted_price': round(predicted_price, 2),
            'confidence': min(round(metrics['r2'] * 100, 1), 99.9)
        })

    return {
        'predictions': predictions,
        'model_metrics': metrics
    }