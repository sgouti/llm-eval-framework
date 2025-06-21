import ollama
from .base_model import BaseModel
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

class OllamaHandler(BaseModel):
    def __init__(self, model_name):
        self.model_name = model_name
        try:
            self.client = ollama.Client(host="http://localhost:11434")
        except Exception as e:
            logger.error(f"Failed to initialize Ollama client: {str(e)}")
            raise

    def generate_response(self, input_text, **kwargs):
        try:
            response = self.client.chat(
                model=self.model_name,
                messages=[{"role": "user", "content": input_text}]
            )
            return response["message"]["content"]
        except Exception as e:
            logger.error(f"Error generating response with {self.model_name}: {str(e)}")
            return f"Error generating response: {str(e)}"