"""Context page layout and content."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from .visuals import render_visuals

def render_page(df: pd.DataFrame, airports_us: pd.DataFrame) -> None:
    """Render the Context page."""

    st.subheader("Context")
    st.write(
        "Use this section to ground the audience in the overall performance of US flights."
    )
    render_visuals(df, airports_us)
