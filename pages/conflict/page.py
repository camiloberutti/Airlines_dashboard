"""Conflict page layout and content."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from .visuals import render_visuals

def render_page(df: pd.DataFrame, airports_us: pd.DataFrame) -> None:
    """Render the Conflict page."""

    st.subheader("Conflict")
    st.write(
        "Highlight the operational issues, delays, and pain points discovered in the data."
    )
    render_visuals(df, airports_us)
