from typing import List

import pandas as pd

from navigation_data_analysis.utils import copy_columns_by_keywords

Valid_Univariate_OD = ["None", "Inner Fence", "Outer Fence"]


def univariate_outlier_detection(
        df: pd.DataFrame,
        method: str,
        excludes: List = None,
        copy: bool = True) -> pd.DataFrame:
    """ Entry point for outlier detection.
    Return the dataframe which the outliers of each column replaced by NULL.

    Parameters
    ----------
    df : pandas DataFrame
        The source dataframe.
    method : str (must be one of the Valid_Univariate_OD)
        The imputation method.
    excludes : list, iterable
        The columns of which the values remain unchanged.
    copy : bool
        If true, guarantee the source dataframe to be unchanged.
    """

    assert method in Valid_Univariate_OD, f"Invalid method: {method}"
    if method == "None":
        return df

    df = df.copy() if copy else df
    df_original = df.copy()

    if method == "Inner Fence":
        df = remove_univariate_outliers(df, 1.5)
    elif method == "Outer Fence":
        df = remove_univariate_outliers(df, 3)
    else:
        raise NotImplementedError

    if excludes:
        df = copy_columns_by_keywords(df_original, df, cols=excludes)

    return df


def remove_univariate_outliers(df: pd.DataFrame, alpha: float) -> pd.DataFrame:
    """ Remove values bigger than upper fence and values smaller than lower fence.
    The removed values are replaced by NULL.
    This function treats each column individually.

    outer fence = Q3 + (alpha * IQR)
    lower fence = Q1 - (alpha * IQR)

    alpha should be pick heuristically between 1.5 and 3

    Reference
    ---------
    https://www.statisticshowto.com/upper-and-lower-fences/#:~:text=Inner%20and%20Outer%20Fences
    """
    Q1 = df.quantile(0.25)
    Q3 = df.quantile(0.75)
    IQR = Q3 - Q1
    outer_fence = Q3 + alpha * IQR
    inner_fence = Q1 - alpha * IQR
    mask = (df > outer_fence) | (df < inner_fence)

    df = df.where(~mask)
    return df
