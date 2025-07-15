import streamlit as st

st.title("About this Dashboard")

st.markdown(
    "This dashboard visualizes UK property investment metrics using a map-based interface. "
    "Data originates from the provided CSV files and postcodes are geocoded using the pgeocode library."
)
