from .base_evaluator import BaseEvaluator
from deepeval.metrics import GEval
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

class DeepEvalEvaluator(BaseEvaluator):
    def __init__(self):
        self.metric = GEval()

    def evaluate(self, input_text, expected_output, response_text, **kwargs):
        try:
            result = self.metric.evaluate(
                prompt=input_text,
                expected_output=expected_output,
                model_output=response_text
            )
            return {"score": result.score, "details": result.reasoning}
        except Exception as e:
            logger.error(f"DeepEval evaluation error: {str(e)}")
            return {"score": 0.0, "details": f"Evaluation error: {str(e)}"}