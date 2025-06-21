from abc import ABC, abstractmethod

class BaseEvaluator(ABC):
    @abstractmethod
    def evaluate(self, input_text, expected_output, response_text, **kwargs):
        pass