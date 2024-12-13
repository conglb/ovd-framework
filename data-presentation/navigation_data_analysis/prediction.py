import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
import plotly.express as px


def mean_absolute_error(groundtruth: pd.Series, prediction: np.array) -> pd.Series:
    groundtruth = groundtruth.copy()
    error = (groundtruth - prediction).abs().mean()
    return error


def Regression(df: pd.DataFrame, target_column: str, prediction_model: str):
    """ Train a Regression Model and return its performace

    Args:
        df (pd.DataFrame): input data
        target_column (str): target of predicting model
        prediction_model (str): name of the used ML model

    Returns:
        _type_: (model, error, score, fig)
    """
    X = df.drop(target_column, axis=1)
    y = df[target_column]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2) # change number here
    X_train, X_test = X_train.sort_index(), X_test.sort_index()
    y_train, y_test = y_train.sort_index(), y_test.sort_index()

    if prediction_model == "Linear Regression":
        model = LinearRegression()
    elif prediction_model == "SVM":
        model = svm.SVR()
    elif prediction_model == "MLP":
        model = MLPRegressor(max_iter=2000, hidden_layer_sizes=10, alpha=0.1)
    elif prediction_model == "Random Forest":
        model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    prediction = model.predict(X_test)
    error = mean_absolute_error(y_test, prediction)
    score = model.score(X_test, y_test)

    # Plot target_column
    df_plot = pd.DataFrame(columns=[target_column+"_groundtruth", target_column+"_prediction"])
    df_plot[target_column+"_groundtruth"] = y_test
    df_plot[target_column+"_prediction"] = prediction
    fig = px.line(df_plot)
    fig.update_layout(title_text=target_column, title_x=0.5)


    return model, error, score, fig