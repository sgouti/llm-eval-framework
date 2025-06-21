import streamlit as st
from pathlib import Path
from ui.pages.dashboard import show_dashboard
from ui.pages.upload import show_upload_page
from ui.pages.configure import show_configure_page
from ui.pages.reports import show_reports_page
from utils.config import Config
from utils.logger import setup_logger

st.set_page_config(
    page_title="LLM Evaluation Framework",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

logger = setup_logger(__name__)

def initialize_session_state():
    if 'config' not in st.session_state:
        st.session_state.config = Config()
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Dashboard"
    if 'evaluation_results' not in st.session_state:
        st.session_state.evaluation_results = []
    if 'test_cases' not in st.session_state:
        st.session_state.test_cases = []

def render_sidebar():
    st.sidebar.title("🤖 LLM Eval Framework")
    st.sidebar.markdown("---")
    pages = {
        "📊 Dashboard": "Dashboard",
        "📤 Upload Test Cases": "Upload",
        "⚙️ Configure Models": "Configure", 
        "📈 Reports": "Reports"
    }
    selected_page = st.sidebar.selectbox(
        "Navigate to:",
        list(pages.keys()),
        index=list(pages.values()).index(st.session_state.current_page)
    )
    st.session_state.current_page = pages[selected_page]
    if st.session_state.evaluation_results:
        st.sidebar.metric("Total Evaluations", len(st.session_state.evaluation_results))
    if st.session_state.test_cases:
        st.sidebar.metric("Test Cases Loaded", len(st.session_state.test_cases))

def main():
    try:
        initialize_session_state()
        render_sidebar()
        if st.session_state.current_page == "Dashboard":
            show_dashboard()
        elif st.session_state.current_page == "Upload":
            show_upload_page()
        elif st.session_state.current_page == "Configure":
            show_configure_page()
        elif st.session_state.current_page == "Reports":
            show_reports_page()
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()