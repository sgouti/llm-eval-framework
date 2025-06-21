import streamlit as st
from src.data.csv_manager import CSVDataManager
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

def show_dashboard():
    """Display the main dashboard with summary statistics."""
    try:
        st.title("🏠 LLM Evaluation Framework Dashboard")
        st.markdown("Welcome to the LLM Evaluation Framework! Use the sidebar to navigate.")

        # Display summary statistics
        data_manager = CSVDataManager()
        stats = data_manager.get_summary_statistics()

        st.subheader("📊 Summary Statistics")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Evaluations", stats["total_evaluations"])
            st.metric("Total Test Cases", stats["total_test_cases"])
        with col2:
            st.metric("Models Evaluated", len(stats["models_evaluated"]))

        # Display category counts
        if stats["category_counts"]:
            st.subheader("Test Cases by Category")
            st.bar_chart(stats["category_counts"])

        # Display average scores per model
        if stats["average_scores"]:
            st.subheader("Average Scores by Model")
            for model, scores in stats["average_scores"].items():
                with st.expander(f"Model: {model}"):
                    for metric, score in scores.items():
                        st.write(f"{metric.replace('_score', '').title()}: {score:.2f}")

        # Display pass rates
        if stats["pass_rates"]:
            st.subheader("Pass Rates by Metric")
            for metric, rate in stats["pass_rates"].items():
                st.write(f"{metric.replace('_score', '').title()}: {rate:.1f}%")

    except Exception as e:
        logger.error(f"Dashboard error: {str(e)}")
        st.error(f"Error loading dashboard: {str(e)}")