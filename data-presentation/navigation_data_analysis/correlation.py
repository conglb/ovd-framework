import dcor
import numpy as np
import pandas as pd
from scipy import stats

Valid_Correlation = ["Pearson", "Spearmanr", "Distance"]


def correlation(df: pd.DataFrame, method: str) -> pd.DataFrame:
    """ Entry point of correlation. Compute pairwise correlation of columns, excluding NA/null values.

    Return
    ------
    cor_df : pd.DataFrame 
    """
    if method == "Pearson":
        cor_df = df.corr(method="pearson").replace(np.nan, 0)
    elif method == "Spearmanr":
        cor_df = df.corr(method="spearman").replace(np.nan, 0)
    elif method == "Distance":
        cor_mat = distance_correlation_matrix(df.values)
        cor_df = pd.DataFrame(cor_mat, columns=df.columns, index=df.columns)
    else:
        raise NotImplementedError
    return cor_df


def pearson_avg(df: pd.DataFrame) -> pd.Series:
    """ Return the average value of Pearson correlation coefficients for each column
    Example
    -------
    The input dataframe consists 3 columns v1, v2, v3
    The output series is:

    Index   Data
    v1      average( coeff(v1, v2), coeff(v1, v3) )
    v2      average( coeff(v2, v1), coeff(v2, v1) )
    v3      average( coeff(v3, v1), coeff(v3, v1) )

    """
    mat = np.corrcoef(df.values.transpose())
    mat = np.abs(mat)
    p_avg_df = pd.DataFrame(mat, columns=df.columns)
    p_avg_df[p_avg_df > 0.999999] = np.nan  # exclude pearson's coeff = 1
    ss = p_avg_df.mean()
    ss = ss.sort_values(ascending=False)
    ss.name = "coeff"
    return ss


def spearmanr_avg(df: pd.DataFrame) -> pd.Series:
    """ Return the average value of Spearmanr correlation coefficients for each column.
    Example
    -------
    See function pearson_avg

    """
    rho, pval = stats.spearmanr(df.values)
    if type(rho) == float:
        return pd.Series(["Not enough piece of input data"], name="Error", index=["Reason"])
    rho = np.abs(rho)
    s_avg_df = pd.DataFrame(rho, columns=df.columns)
    s_avg_df[s_avg_df > 0.999999] = np.nan  # exclude pearson's coeff = 1
    ss = s_avg_df.mean()
    ss = ss.sort_values(ascending=False)
    ss.name = "coeff"
    return ss


def distance_avg(df: pd.DataFrame) -> pd.Series:
    """ Return the average value of Distance correlation coefficients for each column.
    Example
    -------
    See function pearson_avg

    """
    mat = distance_correlation_matrix(df.values)
    d_avg_df = pd.DataFrame(mat, columns=df.columns)
    d_avg_df[d_avg_df > 0.999999] = np.nan  # exclude pearson's coeff = 1
    ss = d_avg_df.mean()
    ss = ss.sort_values(ascending=False)
    ss.name = "coeff"
    return ss


def distance_correlation_matrix(mat: np.ndarray) -> np.ndarray:
    """ Return distance correlations of a 2D array.
    Each column represents a variable, with observations in the rows.
    """
    assert mat.ndim == 2
    n_var = mat.shape[-1]
    result = np.empty((n_var, n_var))

    for i in range(n_var):
        for j in range(n_var):
            if i == j:
                corr = 1
            elif i > j:
                corr = result[j, i]
            else:
                tmp = mat[:, [i, j]]
                tmp = tmp[~np.isnan(tmp).any(axis=1), :]
                corr = dcor.distance_correlation(tmp[:, 0], tmp[:, 1])
            result[i, j] = corr

    return result
