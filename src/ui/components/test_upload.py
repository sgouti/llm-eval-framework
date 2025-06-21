import streamlit as st
from src.data.csv_manager import CSVDataManager
import pandas as pd

def render_test_upload():
    st.subheader("Upload Test Cases")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            manager = CSVDataManager()
            if manager.save_test_cases(df.to_dict('records')):
                st.session_state.test_cases = df.to_dict('records')
                st.success("Test cases uploaded successfully!")
            else:
                st.error("Failed to upload test cases.")
        except Exception as e:
            st.error(f"Error uploading file: {str(e)}")