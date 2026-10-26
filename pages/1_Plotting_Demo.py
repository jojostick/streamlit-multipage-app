import streamlit as st
import time
import numpy as np

# Configure the page
st.set_page_config(
    page_title="Plotting Demo",
    page_icon="📈"
)

# Page title
st.markdown("# Plotting Demo")
st.sidebar.header("Plotting Demo")

# Introduction
st.write(
    """
    This demo illustrates plotting and animation
    with Streamlit.

    Random numbers are generated to create
    an animated line chart.
    """
)

# Create a progress bar
progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()

# Generate initial random data
data = np.random.randn(1, 1)

# Create an empty chart
chart = st.empty()
chart.line_chart(data)

# Update the chart dynamically
for i in range(1, 101):

    # Generate new random values
    new_rows = data[-1, :] + np.random.randn(5, 1).cumsum(axis=0)

    # Append new rows to existing data
    data = np.concatenate([data, new_rows])

    # Update progress information
    status_text.text(f"{i}% Complete")
    chart.line_chart(data)
    progress_bar.progress(i)

    # Slow down the animation
    time.sleep(0.05)

# Clear the progress bar
progress_bar.empty()

# Allow users to restart the animation
st.button("Re-run")


