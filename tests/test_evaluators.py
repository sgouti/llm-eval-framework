import pytest
import pandas as pd
from src.evaluators.deepeval_evaluator import DeepEvalEvaluator
from src.evaluators.custom_evaluator import CustomGEvalEvaluator

def test_deepeval_evaluator(mocker):
    mock_metric = mocker.patch("deepeval.metrics.GEval")
    mock_metric_instance = mock_metric.return_value
    mock_metric_instance.evaluate.return_value = type("Result", (), {"score": 0.9, "reasoning": "Good match"})()

    evaluator = DeepEvalEvaluator()
    result = evaluator.evaluate("Test input", "Expected output", "Test response")

    assert result["score"] == 0.9
    assert result["details"] == "Good match"

def test_deepeval_evaluator_error(mocker):
    mock_metric = mocker.patch("deepeval.metrics.GEval")
    mock_metric_instance = mock_metric.return_value
    mock_metric_instance.evaluate.side_effect = Exception("Evaluation failed")

    evaluator = DeepEvalEvaluator()
    result = evaluator.evaluate("Test input", "Expected output", "Test response")

    assert result["score"] == 0.0
    assert "Evaluation error" in result["details"]

def test_custom_evaluator_match():
    evaluator = CustomGEvalEvaluator()
    result = evaluator.evaluate("Test input", "Expected output", "Expected output")

    assert result["score"] == 1.0
    assert "Exact match" in result["details"]

def test_custom_evaluator_no_match():
    evaluator = CustomGEvalEvaluator()
    result = evaluator.evaluate("Test input", "Expected output", "Different output")

    assert result["score"] == 0.0
    assert "No match" in result["details"]

def test_custom_evaluator_error():
    evaluator = CustomGEvalEvaluator()
    result = evaluator.evaluate("", "", "")

    assert result["score"] == 0.0
    assert "Invalid input" in result["details"]