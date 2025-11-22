"""Solution page layout and content."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from .visuals import render_visuals

def render_page(df: pd.DataFrame, airports_us: pd.DataFrame) -> None:
    """Render the Solution page."""

    st.subheader("Solution")
    st.write(
        "Recommend mitigations and improvements informed by the conflict findings."
    )
    render_visuals(df, airports_us)
