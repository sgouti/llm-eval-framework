import streamlit as st
import pandas as pd
from src.data.csv_manager import CSVDataManager
from src.utils.report_generator import generate_report
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

def render_results():
    """Render evaluation results and summary report in the Streamlit UI."""
    try:
        st.subheader("Evaluation Results")
        
        # Initialize CSVDataManager
        data_manager = CSVDataManager()
        
        # Load evaluation results
        results_df = data_manager.load_evaluation_results()
        
        if results_df.empty:
            st.info("No evaluation results available. Run an evaluation first.")
            return

        # Display results table
        st.write("**Results Table**")
        display_columns = [
            "test_case_id", "model_name", "model_type", "response_text",
            "correctness_score", "relevancy_score", "status", "evaluation_time"
        ]
        # Filter columns that exist in the DataFrame
        display_columns = [col for col in display_columns if col in results_df.columns]
        st.dataframe(results_df[display_columns])

        # Display summary report
        st.subheader("Summary Report")
        report = generate_report(results_df)
        
        if isinstance(report, str):
            st.warning(report)
        else:
            for entry in report:
                with st.expander(f"Model: {entry['model_name']}"):
                    for key, value in entry.items():
                        if key != 'model_name' and pd.notna(value):
                            st.write(f"{key.replace('_score', '').title()}: {value:.2f}")

        # Display summary statistics
        st.subheader("Summary Statistics")
        stats = data_manager.get_summary_statistics()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Evaluations", stats["total_evaluations"])
            st.metric("Total Test Cases", stats["total_test_cases"])
        with col2:
            st.metric("Models Evaluated", len(stats["models_evaluated"]))
        
        if stats["pass_rates"]:
            st.write("**Pass Rates by Metric**")
            for metric, rate in stats["pass_rates"].items():
                st.write(f"{metric.replace('_score', '').title()}: {rate:.1f}%")

    except Exception as e:
        logger.error(f"Error rendering results: {str(e)}")
        st.error(f"Error displaying results: {str(e)}")