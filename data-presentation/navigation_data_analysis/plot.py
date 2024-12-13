import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px

import navigation_data_analysis as nda
from navigation_data_analysis.imputation import Valid_Imputation, impute
from navigation_data_analysis.utils import var2regex


def availability_fig(df):
    col_to_pct = nda.utils.get_availability(
        df).sort_values(ascending=False).rename("Availability")
    fig = px.histogram(
        col_to_pct, x="Availability", range_x=(0, 1))
    fig.update_layout(
        title_text="Histogram of Availablity among all Variables (Without Imputation)",
        title_x=0.5,
        yaxis_title="# of Variables")
    return fig


def availability_fig_each_variable(df):
    col_to_pct = nda.utils.get_availability(
        df).sort_values(ascending=True).rename("Availability")
    fig = px.bar(
        col_to_pct, x=col_to_pct.index, y=col_to_pct.values)
    fig.update_layout(
        title_text="Histogram of Availablity among each Column (Without Imputation)",
        title_x=0.5,
        yaxis_title="Availability", xaxis_title="Column")
    return fig


def plot_histogram(df_filtered, df_imputed, imputation_method: str, var: str):
    regex = var2regex(var)

    if imputation_method == "None":
        df = df_filtered
    else:
        df_imputed = df_imputed.add_suffix(f"_{imputation_method}")
        df = pd.concat([df_filtered, df_imputed], axis=1)
        df = df.reindex(sorted(df.columns, reverse=True), axis=1)

    df = df.filter(regex=regex)
    fig = px.histogram(df, marginal="box", barmode="group")
    fig.update_layout(
        title_text="Histogram of the Variable",
        title_x=0.5,
        yaxis_title="# of entries",
        xaxis_title="Value")
    return fig


def plot_timeline_fig(
        df_filtered,
        df_imputed,
        imputation_method: str,
        var: str):
    """Plot two lines chart, one from original data, the other from imputed data

    Args:
        df_filtered (Dataframe): original data
        df_imputed (Datagrame): imputed data
        imputation_method (str): the imputation method
        var (str): _description_

    Returns:
        Figure: figure
    """    
    regex = var2regex(var)

    if imputation_method == "None":
        df = df_filtered
    else:
        df_imputed = df_imputed.add_suffix(f"_{imputation_method}")
        df = pd.concat([df_filtered, df_imputed], axis=1)
        df = df.reindex(sorted(df.columns, reverse=True), axis=1)
    df = df.filter(regex=regex)
    fig = px.line(df, markers=True)
    fig.update_layout(
        title_text="Line Graph base on Timestamp, data before and after imputation",
        title_x=0.5,
        yaxis_title="Value")
    return fig


def plot_timeline_fig_multiple(
        dfs: list[pd.DataFrame],
        imputation_method: list[str],
        var: str):
    cmap = dict(zip(Valid_Imputation, [
                "black", "purple", "green", "orange", "blue", "red"]))
    regex = var2regex(var)
    df_plot = []
    colors = []
    for df, method in zip(dfs, imputation_method):
        df = df.filter(regex=regex)
        if method == "None":
            avail = nda.utils.get_availability(df)
            assert avail.size == 1
            avail = avail[0]
            df = df.add_suffix(f"_Raw_Availability: {avail:.2f}")
        else:
            df = df.add_suffix(f"_{method}")
        df_plot.append(df)
        colors.append(cmap[method])
    df_plot = pd.concat(df_plot, axis=1)
    plt.clf()
    fig = px.line(df_plot, color_discrete_sequence=colors)
    fig.update_layout(
        title_text="Line Graph base on Timestamp",
        title_x=0.5,
        yaxis_title="Value")
    return fig

def plot_timeline_fig_compare_multiple_methods(
        df_orginal: pd.DataFrame,
        imputation_method: list[str],
        var: str):
    cmap = dict(zip(Valid_Imputation, [
                "red", "purple", "green", "orange", "blue", "black", "wheat", "navy"]))
    regex = var2regex(var)
    df_plot = []
    colors = []
    for method in imputation_method:
        df = df_orginal.filter(regex=regex)
        if method == "None":
            avail = nda.utils.get_availability(df)
            #assert avail.size == 1
            avail = avail[0]
            df = df.add_suffix(f"_Raw_Availability: {avail:.2f}")
        else:
            df = impute(df, method)
            df = df.add_suffix(f"_{method}")
        df_plot.append(df)
        colors.append(cmap[method])
    df_plot = pd.concat(df_plot, axis=1)
    plt.clf()
    fig = px.line(df_plot, color_discrete_sequence=colors)
    fig.update_layout(
        title_text="Line Graph base on Timestamp comparing Imputation methods",
        title_x=0.5,
        yaxis_title="Value")
    return fig
