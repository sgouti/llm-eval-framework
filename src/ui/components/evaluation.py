import streamlit as st
from src.models.ollama_handler import OllamaHandler
from src.models.bedrock_handler import BedrockHandler
from src.evaluators.deepeval_evaluator import DeepEvalEvaluator
from src.evaluators.custom_evaluator import CustomGEvalEvaluator
from src.data.csv_manager import CSVDataManager

def render_evaluation():
    st.subheader("Run Evaluation")
    if 'model_config' not in st.session_state or 'test_cases' not in st.session_state:
        st.warning("Please configure model and upload test cases first!")
        return
    model_config