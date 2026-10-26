import streamlit as st
import pandas as pd
import altair as alt
from urllib.error import URLError

# Configure the page
st.set_page_config(
    page_title="DataFrame Demo",
    page_icon="📊"
)

# Page title
st.markdown("# DataFrame Demo")
st.sidebar.header("DataFrame Demo")

st.write(
    """
    This demo shows how to use Streamlit to
    visualize Pandas DataFrames.

    Data courtesy of the UN Data Explorer.
    """
)

# Load and cache the dataset
@st.cache_data
def get_UN_data():
    url = (
        "https://streamlit-demo-data."
        "s3-us-west-2.amazonaws.com/agri.csv.gz"
    )

    df = pd.read_csv(url)
    return df.set_index("Region")


try:
    # Load agricultural production data
    df = get_UN_data()

    # Select countries
    countries = st.multiselect(
        "Choose countries",
        list(df.index),
        ["China", "United States of America"]
    )

    if not countries:
        st.warning("Please select at least one country.")

    else:
        # Filter selected countries
        data = df.loc[countries].copy()

        # Convert values into billions
        data = data / 1000000.0

        # Display the data table
        st.subheader("Gross Agricultural Production ($B)")
        st.dataframe(data.sort_index())

        # Prepare data for visualization
        chart_data = data.T.reset_index()

        chart_data = pd.melt(
            chart_data,
            id_vars=["index"],
            var_name="Region",
            value_name="Gross Agricultural Product ($B)"
        )

        chart_data = chart_data.rename(
            columns={"index": "year"}
        )

        # Draw the area chart
        chart = (
            alt.Chart(chart_data)
            .mark_area(opacity=0.3)
            .encode(
                x=alt.X(
                    "year:O",
                    title="Year"
                ),
                y=alt.Y(
                    "Gross Agricultural Product ($B):Q",
                    title="Agricultural Production ($B)",
                    stack=None
                ),
                color=alt.Color(
                    "Region:N",
                    title="Country"
                ),
                tooltip=[
                    "Region:N",
                    "year:O",
                    alt.Tooltip(
                        "Gross Agricultural Product ($B):Q",
                        format=".2f"
                    )
                ]
            )
            .properties(
                height=420,
                title="Agricultural Production by Country"
            )
        )

        st.altair_chart(
            chart,
            use_container_width=True
        )

except (URLError, OSError) as e:
    st.error(f"Unable to load the dataset: {e}")


