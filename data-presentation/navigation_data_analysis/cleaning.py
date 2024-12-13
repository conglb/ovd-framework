from typing import List

import numpy as np
import pandas as pd

from navigation_data_analysis.utils import (copy_columns_by_keywords,
                                            get_availability)


def replace_with_null(df: pd.DataFrame,
                      targets: List = None,
                      excludes: List = None,
                      copy: bool = True) -> pd.DataFrame:
    """ Replace symbols with NULL value in a DataFrame.

    Parameters
    ----------
    df : pandas DataFrame
        The source dataframe.
    targets : list, iterable 
        The symbol to be replaced by NULL. e.g. [0., "-"]
    excludes : list, iterable
        The columns of which the values remain unchanged.
    copy : bool
        If true, guarantee the source dataframe to be unchanged.
    """
    df = df.copy() if copy else df

    df_original = df.copy()
    for t in targets:
        df = df.replace(t, np.nan)

    if excludes:
        df = copy_columns_by_keywords(df_original, df, cols=excludes)
    return df


def filter_by_availability(
        df: pd.DataFrame,
        low: float,
        high: float,
        copy: bool = True) -> pd.DataFrame:
    """ Drop the columns of which the availability fall outside the given range [low, high].
    Ask Prof. Wisam for explaination of 'availability'

    Parameters
    ----------
    df : pandas DataFrame
        The source dataframe.
    low : float (the value should be between 0 and 1)
        The lower bound of availablity.
    high : float (the value should be between 0 and 1)
        The upper bound of availablity.
    copy : bool
        If true, guarantee the source dataframe to be unchanged.
    """
    assert 0 <= low <= 1, ValueError(
        f"value of low must fall in [0, 1]. Given low={low}")
    assert 0 <= high <= 1, ValueError(
        f"value of low must fall in [0, 1]. Given low={high}")

    df = df.copy() if copy else df

    s_col2avail = get_availability(df)  # s_ denotes pd.Series
    col = s_col2avail[lambda x: (x >= low) & (x <= high)].index
    return df[col]


def remove_empty_col(df: pd.DataFrame, copy: bool = True) -> pd.DataFrame:
    df = df.copy() if copy else df
    nan_col = df.isna().all()
    col = nan_col[nan_col is False].index
    return df[col]


def remove_full_col(df: pd.DataFrame) -> pd.DataFrame:
    """ Remove the columns where there are values in every row """
    target_col = df.notna().all()
    col = target_col[target_col is False].index
    return df[col]
