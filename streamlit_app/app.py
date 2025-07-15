import streamlit as st
import pydeck as pdk
import pandas as pd

from utils.data_loader import load_data

st.set_page_config(page_title="UK Property ROI", layout="wide")

st.title("UK Property ROI Map")

with st.spinner("Loading data..."):
    df = load_data()

# Sidebar filters
st.sidebar.header("Filters")
regions = sorted(df['region'].dropna().unique())
selected_regions = st.sidebar.multiselect("Region", regions, default=regions)

categories = sorted(df['yield_category'].dropna().unique())
selected_categories = st.sidebar.multiselect("Yield Category", categories, default=categories)

filtered = df[df['region'].isin(selected_regions) & df['yield_category'].isin(selected_categories)]

# Map layer color based on yield category
color_map = {
    "Very High": [0, 128, 0],
    "High": [34, 139, 34],
    "Medium": [255, 165, 0],
    "Low": [255, 0, 0],
}

# Map yield categories to colors and use a grey default for any unmapped
# values. Using dict.get avoids errors with fillna expecting scalar values.
filtered["color"] = filtered["yield_category"].apply(
    lambda cat: color_map.get(cat, [200, 200, 200])
)

layer = pdk.Layer(
    "ScatterplotLayer",
    data=filtered,
    get_position='[longitude, latitude]',
    get_color='color',
    get_radius=800,
    pickable=True,
)

view_state = pdk.ViewState(latitude=54.5, longitude=-3.4, zoom=5)

st.pydeck_chart(pdk.Deck(map_style="mapbox://styles/mapbox/light-v9",
                         initial_view_state=view_state,
                         layers=[layer],
                         tooltip={"text": "{postcode}\nYield: {yield_category}\nPrice: £{price}"}))

st.markdown(f"### {len(filtered)} properties shown")

if st.checkbox("Show data table"):
    st.dataframe(filtered)
