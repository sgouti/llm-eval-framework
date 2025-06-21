import streamlit as st
from ui.components.results import render_results
from utils.logger import setup_logger

logger = setup_logger(__name__)

def show_reports_page():
    """Display the evaluation results and reports page."""
    try:
        st.title("📈 Evaluation Reports")
        st.markdown("View evaluation results and summary statistics.")
        render_results()
    except Exception as e:
        logger.error(f"Reports page error: {str(e)}")
        st.error(f"Error loading reports page: {str(e)}")