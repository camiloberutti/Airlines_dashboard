"""Conflict page visual components."""

from __future__ import annotations

from typing import List

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def render_visuals(df: pd.DataFrame, airports_us: pd.DataFrame) -> None:
    """Render the Conflict page visuals in Streamlit."""

    st.plotly_chart(create_delay_map(df, airports_us),
                    use_container_width=True)


def create_delay_map(df: pd.DataFrame, airports_us: pd.DataFrame, marker_multiplier: int = 300) -> go.Figure:
    """Build a geospatial view comparing weather vs non-weather delays."""

    df = df.copy()
    df["WEATHER_DELAY"] = df["WEATHER_DELAY"].fillna(0)
    df["ARR_DELAY"] = df["ARR_DELAY"].fillna(0)

    df_weather = df[df["WEATHER_DELAY"] > 0].copy()
    stats_weather = (
        df_weather.groupby("ORIGIN_AIRPORT")["WEATHER_DELAY"].agg(
            ["sum", "mean", "median"]).reset_index()
    )
    stats_weather.columns = ["ORIGIN_AIRPORT", "Total", "Avg", "Median"]
    map_weather = stats_weather.merge(
        airports_us[["IATA", "Latitude", "Longitude", "Airport_Name"]],
        left_on="ORIGIN_AIRPORT",
        right_on="IATA",
    )

    df_other = df[(df["ARR_DELAY"] > 0) & (df["WEATHER_DELAY"] == 0)].copy()
    stats_other = (
        df_other.groupby("ORIGIN_AIRPORT")["ARR_DELAY"].agg(
            ["sum", "mean", "median"]).reset_index()
    )
    stats_other.columns = ["ORIGIN_AIRPORT", "Total", "Avg", "Median"]
    map_other = stats_other.merge(
        airports_us[["IATA", "Latitude", "Longitude", "Airport_Name"]],
        left_on="ORIGIN_AIRPORT",
        right_on="IATA",
    )

    def get_size_list(dataset: pd.DataFrame, col: str, multiplier: int) -> List[float]:
        if dataset.empty:
            return []
        values = dataset[col]
        return (values / values.max() * multiplier).fillna(0).tolist()

    w_lon = map_weather["Longitude"].tolist()
    w_lat = map_weather["Latitude"].tolist()
    w_txt = (map_weather["Airport_Name"] + "<br>Code: " +
             map_weather["ORIGIN_AIRPORT"]).tolist()
    w_custom = map_weather[["Total", "Avg", "Median"]].values
    w_size_tot = get_size_list(map_weather, "Total", marker_multiplier)
    w_size_avg = get_size_list(map_weather, "Avg", marker_multiplier)
    w_size_med = get_size_list(map_weather, "Median", marker_multiplier)

    o_lon = map_other["Longitude"].tolist()
    o_lat = map_other["Latitude"].tolist()
    o_txt = (map_other["Airport_Name"] + "<br>Code: " +
             map_other["ORIGIN_AIRPORT"]).tolist()
    o_custom = map_other[["Total", "Avg", "Median"]].values
    o_size_tot = get_size_list(map_other, "Total", marker_multiplier)
    o_size_avg = get_size_list(map_other, "Avg", marker_multiplier)
    o_size_med = get_size_list(map_other, "Median", marker_multiplier)

    fig = go.Figure()

    fig.add_trace(
        go.Scattergeo(
            lon=w_lon,
            lat=w_lat,
            text=w_txt,
            visible=True,
            name="Weather Delays",
            marker=dict(
                size=w_size_tot,
                color="firebrick",
                opacity=0.6,
                sizemode="area",
                line_width=0.5,
                line_color="black",
            ),
            customdata=w_custom,
            hovertemplate="<b>%{text}</b><br>Total: %{customdata[0]:,.0f}m\n<br>Avg: %{customdata[1]:.1f}m\n<br>Med: %{customdata[2]:.1f}m<extra></extra>",
        )
    )

    fig.add_trace(
        go.Scattergeo(
            lon=o_lon,
            lat=o_lat,
            text=o_txt,
            visible=False,
            name="Non-Weather Delays",
            marker=dict(
                size=o_size_tot,
                color="royalblue",
                opacity=0.6,
                sizemode="area",
                line_width=0.5,
                line_color="black",
            ),
            customdata=o_custom,
            hovertemplate="<b>%{text}</b><br>Total: %{customdata[0]:,.0f}m\n<br>Avg: %{customdata[1]:.1f}m\n<br>Med: %{customdata[2]:.1f}m<extra></extra>",
        )
    )

    fig.update_layout(
        height=600,
        title=dict(text="Delay Analysis", y=0.98, x=0.5, xanchor="center"),
        geo=dict(
            scope="usa",
            projection_type="albers usa",
            showland=True,
            landcolor="rgb(230, 230, 230)",
        ),
        margin=dict(t=30, l=0, r=0, b=0),
        updatemenus=[
            dict(
                type="buttons",
                direction="left",
                x=0.01,
                y=1.0,
                xanchor="left",
                yanchor="top",
                bgcolor="rgba(255, 255, 255, 0.9)",
                buttons=[
                    dict(
                        label="Weather Only",
                        method="update",
                        args=[{"visible": [True, False]}, {
                            "title": "Analysis: Weather Delays"}],
                    ),
                    dict(
                        label="Non-Weather",
                        method="update",
                        args=[{"visible": [False, True]}, {
                            "title": "Analysis: Non-Weather Arrival Delays"}],
                    ),
                ],
            ),
            dict(
                type="buttons",
                direction="left",
                x=0.01,
                y=0.01,
                xanchor="left",
                yanchor="bottom",
                bgcolor="rgba(255, 255, 255, 0.9)",
                active=2,
                buttons=[
                    dict(label="Median", method="restyle", args=[
                         ["marker.size"], [[w_size_med, o_size_med]]]),
                    dict(label="Average", method="restyle", args=[
                         ["marker.size"], [[w_size_avg, o_size_avg]]]),
                    dict(label="Total", method="restyle", args=[
                         ["marker.size"], [[w_size_tot, o_size_tot]]]),
                ],
            ),
        ],
    )

    return fig
