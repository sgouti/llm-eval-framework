import streamlit as st
from src.ui.components.model_config import render_model_config
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

def show_configure_page():
    """Display the model configuration page."""
    try:
        st.title("⚙️ Configure Models")
        st.markdown("Select a model type and specific model to use for evaluations.")
        render_model_config()
    except Exception as e:
        logger.error(f"Configure page error: {str(e)}")
        st.error(f"Error loading configure page: {str(e)}")