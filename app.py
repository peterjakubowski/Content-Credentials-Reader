import streamlit as st
from services.reader import read_content_credentials
from components.streamlit_workflow import streamlit_workflow


def app():

    st.title("Content Credentials Reader")

    st.write("Upload an image to summarize its content credentials.")

    file = st.file_uploader(
        label="upload",
        label_visibility="hidden",
        accept_multiple_files=False,
        type=["jpg", "jpeg", "png", "tif"],
        key="upload"
    )

    if file:
        if read_content_credentials(file):
            streamlit_workflow()

# Run the app
app()
