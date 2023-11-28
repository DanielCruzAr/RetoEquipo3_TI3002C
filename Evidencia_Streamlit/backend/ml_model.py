import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from datetime import timedelta

def parse_data(data):
    colums = ['fecha', 'salidas', 'existencias']
    df_product = data[colums]
    df_product["fecha"] = pd.to_datetime(df_product["fecha"])
    df_product["ordinal"] = df_product["fecha"].apply(lambda x: x.toordinal())
    df_product = df_product.sort_values(by='fecha')
    df_product.set_index("fecha", inplace=True)
    return df_product

def predict(train, test, predictors, model):
    model.fit(train[predictors], train["Target"])
    preds = model.predict(test[predictors])
    preds = pd.Series(preds, index=test.index, name="preds")
    combined = pd.concat([test["Target"], preds], axis=1)
    return combined

def backtest(data, model, predictors, start, step):
    all_predictions = []

    for i in range(start, data.shape[0], step):
        train = data.iloc[0:i].copy()
        test = data.iloc[i:i+step].copy()
        predictions = predict(train, test, predictors, model)
        all_predictions.append(predictions)
    return pd.concat(all_predictions)

def train_model_1(df_product, model, predictors):
    df_product_1 = df_product.copy()
    df_product_1["Target"] = df_product_1["existencias"].shift(-1)
    df_product_1.dropna(inplace=True)
    predictions = backtest(df_product_1, model, predictors, 30, 30)
    return predictions

def train_model_2(df_product, model, predictors):
    df_product_2 = df_product.copy()
    df_product_2["Target"] = df_product_2["salidas"].shift(-1)
    df_product_2.dropna(inplace=True)
    predictions = backtest(df_product_2, model, predictors, 30, 30)
    return predictions

def make_predictions(df_product, model1, model2, mae):
    df_target = df_product.copy()
    df_target["lim_sup"] = np.nan
    df_target["lim_inf"] = np.nan
    predictors = ['salidas', 'existencias', 'ordinal']

    start = 30
    step = 30

    for i in range(start, df_target.shape[0], step):
        data = df_target[predictors].iloc[0:i].copy()
        next_existencias = model1.predict(data)
        next_salidas = model2.predict(data)
        next_day = df_target.index[-1] + timedelta(days=1)
        
        df_target = pd.concat([df_target, pd.DataFrame({
                                    "existencias": next_existencias[-1], 
                                    "salidas": next_salidas[-1],
                                    "ordinal": next_day.toordinal(),
                                    "lim_sup": next_existencias[-1] + mae,
                                    "lim_inf": next_existencias[-1] - mae}, 
                                    index=[next_day])])
        
    return df_target

def predict_next_month(data):
    df_product = parse_data(data)
    model1 = RandomForestRegressor(n_estimators=100, min_samples_leaf=10, random_state=1)
    model2 = RandomForestRegressor(n_estimators=100, min_samples_leaf=10, random_state=1)
    
    predictors = ['salidas', 'existencias', 'ordinal']
    predictions1 = train_model_1(df_product, model1, predictors)
    predictions2 = train_model_2(df_product, model2, predictors)
    mae1 = mean_absolute_error(predictions1["Target"], predictions1["preds"])

    df_target = make_predictions(df_product, model1, model2, mae1)
    return df_target