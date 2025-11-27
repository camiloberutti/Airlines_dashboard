"""Best Airline Suggester visual components."""

from __future__ import annotations
import plotly.graph_objects as go

from typing import Tuple

import pandas as pd
import streamlit as st

<< << << < HEAD

== == == =
>>>>>> > 2d87f92f8ade310b0b4f0dbd74013cdbb40b6457


def render_visuals(df: pd.DataFrame, airports_us: pd.DataFrame) -> None:
    """Render interactive airline recommendations for a chosen route."""

    st.subheader("Route-specific performance ranking")
    if df.empty:
        st.info("No flight records available. Load data to unlock suggestions.")
        return


<< << << < HEAD
   # Build airport lookup by IATA to display full names
   airports_lookup = {}
    if airports_us is not None and not airports_us.empty:
        for _, r in airports_us.iterrows():
            iata = r.get("IATA")
            name = r.get("Airport_Name")
            city = r.get("City")
            state = r.get("State")
            airports_lookup[iata] = {
                "name": name,
                "city": city,
                "state": state,
            }

    # State selector to filter origin airports
    states = [s for s in sorted(
        {v.get("state") for v in airports_lookup.values() if v.get("state")})]
    states_options = ["All states"] + states
    state_choice = st.selectbox(
        "Filter by state (origin)", states_options, index=0, key="best_airline_state")

    # Build list of origins (IATA) present in dataset, optionally filter by state
    origin_iatas = sorted(df["ORIGIN_AIRPORT"].dropna().unique())
    if state_choice != "All states":
        origin_iatas = [
            i for i in origin_iatas if i in airports_lookup and airports_lookup[i]["state"] == state_choice]

    # Map to readable labels: "IATA — Airport Name (City)"
    label_by_iata = {}
    origin_labels = []
    for i in origin_iatas:
        info = airports_lookup.get(i)
        if info:
            label = f"{i} — {info['name']} ({info['city']})"
        else:
            label = str(i)
        label_by_iata[label] = i
        origin_labels.append(label)

    if not origin_labels:
        st.warning("No airports available for the selected state.")
        return

    origin_label_choice = st.selectbox(
        "Origin airport", origin_labels, index=0, key="best_airline_origin")
    origin_choice = label_by_iata[origin_label_choice]

    # Available destinations from the selected IATA code
    dest_iatas = sorted(df.loc[df["ORIGIN_AIRPORT"] ==
                        origin_choice, "DEST_AIRPORT"].dropna().unique())
    # Map destinations to readable labels
    dest_label_by_iata = {}
    dest_labels = []
    for i in dest_iatas:
        info = airports_lookup.get(i)
        if info:
            label = f"{i} — {info['name']} ({info['city']})"
        else:
            label = str(i)
        dest_label_by_iata[label] = i
        dest_labels.append(label)
    if not dest_labels:
        st.warning("This origin airport has no destinations in the dataset.")
        return

    destination_label_choice = st.selectbox(
        "Destination airport",
        dest_labels,
        index=0,
        key="best_airline_destination",
    )
    destination_choice = dest_label_by_iata[destination_label_choice]
== == == =
   origins = sorted(df["ORIGIN_AIRPORT"].dropna().unique())
    origin_choice = st.selectbox(
        "Origin airport",
        origins,
        index=0,
        key="best_airline_origin",
    )
    destinations = sorted(
        df.loc[df["ORIGIN_AIRPORT"] == origin_choice,
               "DEST_AIRPORT"].dropna().unique()
    )
    if not destinations:
        st.warning(
            "This origin currently has no destination records in the dataset.")
        return

    destination_choice = st.selectbox(
        "Destination airport",
        destinations,
        index=0,
        key="best_airline_destination",
    )
>>>>>> > 2d87f92f8ade310b0b4f0dbd74013cdbb40b6457

   recommendations, sample_size, weeks_observed = _get_route_recommendations(
        df, origin_choice, destination_choice
    )

    if sample_size == 0:
        st.warning("No flights found for the selected route.")
        return

    left, middle, right = st.columns(3)
    left.metric("Flights analyzed", f"{sample_size:,}")
    middle.metric("Weeks of data", weeks_observed if weeks_observed else "–")
    if not recommendations.empty:
        right.metric(
            "Best avg arrival delay",
            f"{recommendations.iloc[0]['Avg Arrival Delay (min)']:.1f} min",
        )
    else:
        right.metric("Best avg arrival delay", "–")

    if recommendations.empty:
        st.info(
            "Every airline on this route has very few flights in the selected period."
        )
        return

    total_weekly = recommendations['Flights / Week'].sum()
    st.write(
        f"Top {len(recommendations)} airlines for this route (about {total_weekly:.1f} flights/week combined)."
    )
    st.dataframe(recommendations, width="stretch")
    st.caption(
        "Avg delays below zero mean the airline typically arrives ahead of schedule. Flights/week reflects only the weeks present in the dataset."
    )

<< << << < HEAD
   # Summary chart based on the recommendations table
   try:
        # Bar: Flights / Week, Line: Avg Arrival Delay (min) on secondary axis
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=recommendations["Airline"],
            y=recommendations["Flights / Week"],
            name="Flights / Week",
            marker_color="steelblue",
        ))

        fig.add_trace(go.Scatter(
            x=recommendations["Airline"],
            y=recommendations["Avg Arrival Delay (min)"],
            name="Avg Arrival Delay (min)",
            yaxis="y2",
            mode="lines+markers",
            marker=dict(color="firebrick"),
        ))

        fig.update_layout(
            title="Summary: flights/week vs average delay",
            xaxis=dict(title="Airline"),
            yaxis=dict(title="Flights / Week", side="left"),
            yaxis2=dict(title="Avg Arrival Delay (min)",
                        overlaying="y", side="right"),
            legend=dict(orientation="h", yanchor="bottom",
                        y=1.02, xanchor="right", x=1),
            margin=dict(t=60, b=20),
            height=380,
        )

        st.plotly_chart(fig, use_container_width=True)
    except Exception:
        # If plotly is not available for some reason, do not break the page
        st.info("Install `plotly` to view the chart (pip install plotly).")

== =====
>>>>>> > 2d87f92f8ade310b0b4f0dbd74013cdbb40b6457


def _get_route_recommendations(
    df: pd.DataFrame,
    origin: str,
    destination: str,
) -> Tuple[pd.DataFrame, int, int]:
    """Return the best-performing airlines on the specified route."""

    route_df = df[(df["ORIGIN_AIRPORT"] == origin) & (
        df["DEST_AIRPORT"] == destination)].copy()
    if route_df.empty:
        return pd.DataFrame(), 0, 0

    if not pd.api.types.is_datetime64_any_dtype(route_df["FL_DATE"]):
        route_df["FL_DATE"] = pd.to_datetime(route_df["FL_DATE"])

    route_df["YearWeek"] = route_df["FL_DATE"].dt.to_period("W")
    weeks_observed = max(int(route_df["YearWeek"].nunique()), 1)

    grouped = (
        route_df.groupby(["AIRLINE_ID", "Airline_Name"], dropna=False)
        .aggregate(
            Flights=("ARR_DELAY", "size"),
            AvgArrivalDelay=("ARR_DELAY", "mean"),
            OnTimeRate=("ARR_DELAY", lambda s: (s <= 0).mean()),
        )
        .reset_index()
    )

    weeks_per_airline = (
        route_df.groupby("AIRLINE_ID")["YearWeek"].nunique(
        ).reset_index(name="WeeksWithFlights")
    )
    grouped = grouped.merge(weeks_per_airline, on="AIRLINE_ID", how="left")
    grouped["WeeksWithFlights"] = grouped["WeeksWithFlights"].clip(lower=1)
    grouped["FlightsPerWeek"] = (
        grouped["Flights"] / grouped["WeeksWithFlights"]).round(1)

    grouped = grouped.sort_values(
        by=["AvgArrivalDelay", "OnTimeRate"], ascending=[True, False]
    ).head(3)
    grouped["On-Time %"] = (grouped["OnTimeRate"] * 100).round(1)
    grouped = grouped.rename(
        columns={
            "Airline_Name": "Airline",
            "AvgArrivalDelay": "Avg Arrival Delay (min)",
        }
    )

    return (
        grouped[
            [
                "Airline",
                "FlightsPerWeek",
                "On-Time %",
                "Avg Arrival Delay (min)",
            ]
        ]
        .rename(columns={"FlightsPerWeek": "Flights / Week"})
        .reset_index(drop=True),
        len(route_df),
        weeks_observed,
    )
