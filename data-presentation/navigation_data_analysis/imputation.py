from typing import List

import pandas as pd
from sklearn.impute import KNNImputer

from navigation_data_analysis.utils import copy_columns_by_keywords

Valid_Imputation = ["None", "Nearest",
                    "KNN",
                    "Mean",
                    "Linear",
                    "Time Linear",
                    "Drop Row", "Last Observation", "Next Observation",
                    'Last&Next Observation', "Next&Last Observation"]


def impute(df: pd.DataFrame,
           method: str,
           excludes: List = None,
           copy: bool = True) -> pd.DataFrame:
    """ Entry point for any approach of imputation. Return the imputed dataframe.
    
    - Drop rows: removes every rows that contains at least one NULL values
    - Linear
    - Time linear
    - KNN
    - Mean

    Parameters
    ----------
    df : pandas DataFrame
        The source dataframe.
    method : str (must be one of the Valid_Imputation)
        The imputation method.
    excludes : list, iterable
        The columns of which the values remain unchanged.
    copy : bool
        If true, guarantee the source dataframe to be unchanged.
    """

    assert method in Valid_Imputation, f"Invalid method: {method}"
    if method == "None":
        return df

    df = df.copy() if copy else df
    df_original = df.copy()

    if method == "KNN":
        df = _knn_imputation(df)
    elif method == "Linear":
        df = df.interpolate("linear", limit=None, limit_direction='both')
    elif method == "Time Linear":
        df = df.interpolate("time", limit=None, limit_direction='both')
    elif method == "Mean":
        df = df.fillna(df.mean())
    elif method == "Drop Row": 
        df = df.dropna()
    elif method == "Last Observation":
        df = df.fillna(method = 'bfill')
    elif method == "Next Observation":
        df = df.fillna(method = 'ffill')
    elif method == "Nearest":
        df = df.interpolate("nearest", limit=None, limit_direction='both', fill_value='extrapolate')
    if excludes:
        df = copy_columns_by_keywords(df_original, df, cols=excludes)
    return df


def _knn_imputation(df: pd.DataFrame) -> pd.DataFrame:
    """ Wrapper of sklearn KNNImputer that works with a dataframe"""
    imputer = KNNImputer(n_neighbors=5)
    arr_imputed = imputer.fit_transform(df)
    return pd.DataFrame(arr_imputed, columns=df.columns, index=df.index)
