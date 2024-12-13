import re
from typing import List

import pandas as pd

from navigation_data_analysis.heuristic_dict import GROUP_DICT


def var2regex(var: str) -> str:
    """" Transform a variable name to python regular expression """
    regex = "^" + var.replace(
        "(", "\\(").replace(")", "\\)").replace(" ", "\\s")
    regex = re.compile(regex, re.IGNORECASE)
    return regex


def copy_columns_by_keywords(df_src: pd.DataFrame,
                             df_tgt: pd.DataFrame,
                             cols: List) -> pd.DataFrame:
    """ Copy column values fromm the source dataframe to the target dataframe.

    Parameters
    ----------
    df_src : pandas DataFrame
        The source dataframe.
    df_tgt : list, iterable
        The target dataframe.
    cols : list, iterable
        The columns in which the values are copied.
    """
    for c in cols:
        target = df_src.filter(regex=var2regex(c))
        for c_ in target.columns:
            df_tgt[c_] = df_src[c_]
    return df_tgt


def get_availability(df: pd.DataFrame) -> pd.Series:
    """ Return the availability of each column in the source dataframe """
    n_rows = len(df)
    n_data = df.notna().sum()
    s_col2avail = n_data / n_rows
    return s_col2avail


def normalize(df: pd.DataFrame, copy: bool = True) -> pd.DataFrame:
    df = df.copy() if copy else df
    mean, std = df.mean(), df.std()
    std[std == 0] = 1  # std == 0 leads to divided-by-zero error
    df_normalized = (df - mean) / std
    return df_normalized


def select_by_group(df: pd.DataFrame, group: str, copy: bool = True):
    """ Return dataframe with columns belongs to pre-defined group.

    Parameters
    ----------
    df : pandas DataFrame
        The source dataframe.
    group : str (Must be one of the keys in GROUP_DICT)
        Pre-defined group name of columns.
    copy : bool
        If true, guarantee the source dataframeto be unchanged.

    Returns
    -------
    df : pandas DataFrame
        Processed dataframe.

    cols_not_found : List[str]
        The col_names that defined in group but not in source dataframe.
    """
    df = df.copy() if copy else df

    if group == "All":
        cols_not_found = []
        return df, cols_not_found
    return select_cols(df, GROUP_DICT[group], copy=False)


def select_cols(df: pd.DataFrame, cols: List[str], copy: bool = True):
    """ Return dataframe with given column names.

    Parameters
    ----------
    df : pandas DataFrame
        The source dataframe.
    cols : List[str]
        Name of columns to be reserved in the source dataframe.
    copy : bool
        If true, guarantee the source dataframe to be unchanged.

    Returns
    -------
    df : pandas DataFrame
        Processed dataframe.

    cols_not_found : List[str]
        The col_names that defined in group but not in source dataframe.
    """

    df = df.copy() if copy else df

    result = []
    cols_not_found = []
    for c in cols:
        target = df.filter(regex=var2regex(c))
        if target.empty:
            cols_not_found.append(c)
            continue
        for c_ in target.columns:
            result.append(target[c_])
    df_result = pd.concat(result, axis=1)
    # Remove duplicate columns without checking the values
    df_result = df_result.loc[:, ~df_result.columns.duplicated()]
    # More details
    # https://stackoverflow.com/questions/14984119/python-pandas-remove-duplicate-columns
    return df_result, cols_not_found


def select_rows(df: pd.DataFrame, rows: List[str], copy: bool = True):
    """ Return dataframe with given row names.

    See function select_columns
    """
    df = df.copy() if copy else df
    result = []
    rows_not_found = []
    for r in rows:
        target = df.filter(regex=var2regex(r), axis=0)
        if target.empty:
            rows_not_found.append(r)
        for r_ in target.index:
            result.append(target.loc[[r_]])
    df_result = pd.concat(result, axis=0)
    # Remove duplicate columns without checking the values
    df_result = df_result.loc[~df_result.index.duplicated(keep='first')]
    # More details
    # https://stackoverflow.com/questions/14984119/python-pandas-remove-duplicate-columns
    return df_result, rows_not_found


def select_by_state(df: pd.DataFrame, state: str) -> pd.DataFrame:
    """ Return dataframe with the rows where state equals to specific state.

    Parameters
    ----------
    df : pandas DataFrame
        The source dataframe.
    state : str (Must be one of the keys in Valid_State)
        A state of the vessel.
    copy : bool
        If true, guarantee the source dataframe to be unchanged.
    """

    Valid_State = ["All", "At Anchor", "In Port",
                   "Drifting", "At Sea", "Manoeuvring"]
    assert state in Valid_State, ValueError(
        f"State must be one of {Valid_State}. Given State:{state}")

    if state == "All":
        return df
    return df.loc[df['State'] == state]
