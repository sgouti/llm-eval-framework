import streamlit as st
from src.utils.config import Config

def render_model_config():
    st.subheader("Configure Models")
    config = Config()
    model_type = st.selectbox("Model Type", ["ollama", "bedrock"])
    try:
        if model_type == "ollama":
            model_name = st.selectbox("Ollama Model", config.get_available_ollama_models())
        else:
            model_name = st.selectbox("Bedrock Model", config.get_available_bedrock_models())
        if st.button("Save Configuration"):
            st.session_state.model_config = {"type": model_type, "name": model_name}
            st.success("Model configured!")
    except Exception as e:
        st.error(f"Error configuring model: {str(e)}")