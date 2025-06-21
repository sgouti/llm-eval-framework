from .base_evaluator import BaseEvaluator
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

class CustomGEvalEvaluator(BaseEvaluator):
    def evaluate(self, input_text, expected_output, response_text, **kwargs):
        try:
            if not input_text or not expected_output or not response_text:
                return {"score": 0.0, "details": "Invalid input: empty text provided"}
            
            # Simple exact match evaluation for demonstration
            if response_text.strip().lower() == expected_output.strip().lower():
                return {"score": 1.0, "details": "Exact match"}
            else:
                return {"score": 0.0, "details": "No match"}
        except Exception as e:
            logger.error(f"Custom evaluation error: {str(e)}")
            return {"score": 0.0, "details": f"Evaluation error: {str(e)}"}