"""Streamlit entrypoint for the airline visualization project."""

from __future__ import annotations

from pathlib import Path
from typing import Callable, Dict, Tuple

import pandas as pd
import streamlit as st

from preprocess import load_preprocessed_data
from pages.context import render_page as render_context_page
from pages.conflict import render_page as render_conflict_page
from pages.solution import render_page as render_solution_page

st.set_page_config(
    page_title="US Airline Operations",
    page_icon="✈️",
    layout="wide",
)


@st.cache_data(show_spinner="Loading flight and airport data...")
def get_data(dataset_path: str | Path = "Airline_dataset.csv") -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Cache the preprocessing step so Streamlit reloads stay fast."""

    return load_preprocessed_data(dataset_path)


PAGES: Dict[str, Callable[[pd.DataFrame, pd.DataFrame], None]] = {
    "Context": render_context_page,
    "Conflict": render_conflict_page,
    "Solution": render_solution_page,
}


def main() -> None:
    df, airports_us = get_data()

    st.title("Flight Reliability & Resilience Dashboard")
    selected_page = st.sidebar.radio("Navigate", list(PAGES.keys()), index=0)

    PAGES[selected_page](df, airports_us)


if __name__ == "__main__":
    main()
