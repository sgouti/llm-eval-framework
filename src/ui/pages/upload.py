import streamlit as st
from ui.components.test_upload import render_test_upload
from utils.logger import setup_logger

logger = setup_logger(__name__)

def show_upload_page():
    """Display the test case upload page."""
    try:
        st.title("📤 Upload Test Cases")
        st.markdown("Upload a CSV file containing test cases with columns: id, input_text, expected_output, category, tags.")
        render_test_upload()
    except Exception as e:
        logger.error(f"Upload page error: {str(e)}")
        st.error(f"Error loading upload page: {str(e)}")