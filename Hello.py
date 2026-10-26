import streamlit as st

# Configure the home page
st.set_page_config(
    page_title="Hello",
    page_icon="👋"
)

# Main title
st.write("# Welcome to Streamlit! 👋")

# Sidebar message
st.sidebar.success("Select a demo above.")

# Introduction
st.markdown(
    """
    Streamlit is an open-source app framework built
    specifically for Machine Learning and Data Science.

    **Select a demo from the sidebar** to explore
    different Streamlit features!

    ### Available Pages

    - Plotting Demo: Interactive charts and animation.
    - Mapping Demo: Geographic data visualization.
    - DataFrame Demo: Data analysis and tables.

    ### Want to learn more?

    - [Streamlit Website](https://streamlit.io)
    - [Documentation](https://docs.streamlit.io)
    - [Community Forum](https://discuss.streamlit.io)
    """
)

