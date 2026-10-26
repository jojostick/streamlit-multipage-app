import streamlit as st
import pandas as pd
import pydeck as pdk
from urllib.error import URLError

# Configure the page
st.set_page_config(
    page_title="Mapping Demo",
    page_icon="🌍"
)

st.markdown("# Mapping Demo")
st.sidebar.header("Mapping Demo")

st.write(
    """
    This demo shows how to use Streamlit and PyDeck
    to display interactive geographic data.
    """
)

# Load and cache geographic datasets
@st.cache_data
def from_data_file(filename):
    url = (
        "https://raw.githubusercontent.com/streamlit/"
        "example-data/master/hello/v1/" + filename
    )
    return pd.read_json(url)


try:
    # Define map layers
    ALL_LAYERS = {
        "Bike Rentals": pdk.Layer(
            "HexagonLayer",
            data=from_data_file("bike_rental_stats.json"),
            get_position=["lon", "lat"],
            radius=200,
            elevation_scale=4,
            elevation_range=[0, 1000],
            extruded=True,
        ),

        "Bart Stop Exits": pdk.Layer(
            "ScatterplotLayer",
            data=from_data_file("bart_stop_stats.json"),
            get_position=["lon", "lat"],
            get_color=[200, 30, 0, 160],
            get_radius="exits",
            radius_scale=0.05,
        ),

        "Bart Stop Names": pdk.Layer(
            "TextLayer",
            data=from_data_file("bart_stop_stats.json"),
            get_position=["lon", "lat"],
            get_text="name",
            get_color=[0, 0, 0, 200],
            get_size=15,
            get_alignment_baseline="'bottom'",
        ),

        "Outbound Flow": pdk.Layer(
            "ArcLayer",
            data=from_data_file("bart_path_stats.json"),
            get_source_position=["lon", "lat"],
            get_target_position=["lon2", "lat2"],
            get_source_color=[200, 30, 0, 160],
            get_target_color=[200, 30, 0, 160],
            auto_highlight=True,
            width_scale=0.0001,
            get_width="outbound",
            width_min_pixels=3,
            width_max_pixels=30,
        ),
    }

    # Add checkboxes for map layers
    st.sidebar.markdown("### Map Layers")

    selected_layers = [
        layer
        for layer_name, layer in ALL_LAYERS.items()
        if st.sidebar.checkbox(layer_name, True)
    ]

    # Display the interactive map
    if selected_layers:
        st.pydeck_chart(
            pdk.Deck(
                map_style=None,
                initial_view_state=pdk.ViewState(
                    latitude=37.76,
                    longitude=-122.4,
                    zoom=11,
                    pitch=50,
                ),
                layers=selected_layers,
            )
        )
    else:
        st.warning("Please select at least one map layer.")

except (URLError, OSError) as e:
    st.error(f"Unable to load map data: {e}")


