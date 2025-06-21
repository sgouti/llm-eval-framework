import pytest
import pandas as pd
from src.data.csv_manager import CSVDataManager
from src.utils.config import Config

@pytest.fixture
def data_manager(tmp_path):
    """Create a CSVDataManager instance with a temporary directory."""
    return CSVDataManager(data_dir=tmp_path)

def test_save_and_load_test_cases(data_manager):
    """Test saving and loading test cases."""
    test_cases = [
        {"id": 1, "input_text": "Hello", "expected_output": "Hi", "category": "greeting", "tags": "positive"}
    ]
    assert data_manager.save_test_cases(test_cases)
    loaded = data_manager.load_test_cases()
    assert len(loaded) == 1
    assert loaded.iloc[0]["input_text"] == "Hello"
    assert loaded.iloc[0]["category"] == "greeting"
    assert loaded.iloc[0]["tags"] == "positive"

def test_load_empty_test_cases(data_manager):
    """Test loading test cases when the file doesn't exist."""
    loaded = data_manager.load_test_cases()
    assert loaded.empty
    assert set(loaded.columns) == {'id', 'input_text', 'expected_output', 'context', 'category', 'tags', 'created_at', 'updated_at'}

def test_add_test_case(data_manager):
    """Test adding a single test case."""
    test_case = {"input_text": "Hello", "expected_output": "Hi", "category": "greeting"}
    assert data_manager.add_test_case(test_case)
    loaded = data_manager.load_test_cases()
    assert len(loaded) == 1
    assert loaded.iloc[0]["id"] == 1
    assert loaded.iloc[0]["input_text"] == "Hello"
    assert loaded.iloc[0]["category"] == "greeting"

def test_save_and_load_evaluation_results(data_manager):
    """Test saving and loading evaluation results."""
    results = [
        {
            "test_case_id": 1,
            "model_name": "llama3:8b",
            "model_type": "ollama",
            "response_text": "Hi there",
            "correctness_score": 0.9,
            "relevancy_score": 0.95,
            "status": "success"
        }
    ]
    assert data_manager.save_evaluation_results(results)
    loaded = data_manager.load_evaluation_results()
    assert len(loaded) == 1
    assert loaded.iloc[0]["model_name"] == "llama3:8b"
    assert loaded.iloc[0]["correctness_score"] == 0.9
    assert loaded.iloc[0]["relevancy_score"] == 0.95

def test_load_empty_evaluation_results(data_manager):
    """Test loading evaluation results when the file doesn't exist."""
    loaded = data_manager.load_evaluation_results()
    assert loaded.empty
    assert set(loaded.columns) == {
        'id', 'test_case_id', 'model_name', 'model_type', 'response_text',
        'correctness_score', 'relevancy_score', 'fluency_score', 'coherence_score',
        'toxicity_score', 'bias_score', 'custom_metrics', 'evaluation_time',
        'duration_ms', 'status', 'error_message'
    }

def test_get_test_case_by_id(data_manager):
    """Test retrieving a test case by ID."""
    test_cases = [
        {"id": 1, "input_text": "Hello", "expected_output": "Hi", "category": "greeting"}
    ]
    data_manager.save_test_cases(test_cases)
    result = data_manager.get_test_case_by_id(1)
    assert result is not None
    assert result["input_text"] == "Hello"
    assert result["category"] == "greeting"
    assert data_manager.get_test_case_by_id(2) is None

def test_get_results_by_model(data_manager):
    """Test filtering evaluation results by model name."""
    results = [
        {
            "test_case_id": 1,
            "model_name": "llama3:8b",
            "model_type": "ollama",
            "response_text": "Hi there",
            "correctness_score": 0.9
        },
        {
            "test_case_id": 2,
            "model_name": "mistral:7b",
            "model_type": "ollama",
            "response_text": "Hello",
            "correctness_score": 0.8
        }
    ]
    data_manager.save_evaluation_results(results)
    filtered = data_manager.get_results_by_model("llama3:8b")
    assert len(filtered) == 1
    assert filtered.iloc[0]["model_name"] == "llama3:8b"
    assert filtered.iloc[0]["correctness_score"] == 0.9

def test_get_results_by_category(data_manager):
    """Test filtering evaluation results by category."""
    test_cases = [
        {"id": 1, "input_text": "Hello", "expected_output": "Hi", "category": "greeting"},
        {"id": 2, "input_text": "What is 2+2?", "expected_output": "4", "category": "math"}
    ]
    results = [
        {
            "test_case_id": 1,
            "model_name": "llama3:8b",
            "model_type": "ollama",
            "response_text": "Hi there",
            "correctness_score": 0.9
        },
        {
            "test_case_id": 2,
            "model_name": "llama3:8b",
            "model_type": "ollama",
            "response_text": "4",
            "correctness_score": 1.0
        }
    ]
    data_manager.save_test_cases(test_cases)
    data_manager.save_evaluation_results(results)
    filtered = data_manager.get_results_by_category("greeting")
    assert len(filtered) == 1
    assert filtered.iloc[0]["test_case_id"] == 1
    assert filtered.iloc[0]["correctness_score"] == 0.9

def test_calculate_pass_rate(data_manager):
    """Test calculating pass rate for a metric."""
    results = [
        {
            "test_case_id": 1,
            "model_name": "llama3:8b",
            "model_type": "ollama",
            "response_text": "Hi there",
            "correctness_score": 0.9
        },
        {
            "test_case_id": 2,
            "model_name": "llama3:8b",
            "model_type": "ollama",
            "response_text": "Hello",
            "correctness_score": 0.6
        }
    ]
    data_manager.save_evaluation_results(results)
    results_df = data_manager.load_evaluation_results()
    pass_rate = data_manager.calculate_pass_rate(results_df, "correctness_score", 0.7, higher_is_better=True)
    assert pass_rate == 50.0  # One out of two passes (0.9 >= 0.7, 0.6 < 0.7)

def test_calculate_pass_rate_empty(data_manager):
    """Test pass rate calculation with empty data."""
    results_df = data_manager.load_evaluation_results()
    pass_rate = data_manager.calculate_pass_rate(results_df, "correctness_score", 0.7)
    assert pass_rate == 0.0

def test_get_summary_statistics(data_manager, mocker):
    """Test generating summary statistics."""
    # Mock Config to provide consistent thresholds and metrics
    mock_config = mocker.patch("src.utils.config.Config")
    mock_config_instance = mock_config.return_value
    mock_config_instance.get_available_metrics.return_value = {
        "correctness": {"higher_is_better": True},
        "relevancy": {"higher_is_better": True}
    }
    mock_config_instance.metrics_config = {
        "thresholds": {
            "correctness": 0.7,
            "relevancy": 0.8
        }
    }

    test_cases = [
        {"id": 1, "input_text": "Hello", "expected_output": "Hi", "category": "greeting"},
        {"id": 2, "input_text": "What is 2+2?", "expected_output": "4", "category": "math"}
    ]
    results = [
        {
            "test_case_id": 1,
            "model_name": "llama3:8b",
            "model_type": "ollama",
            "response_text": "Hi there",
            "correctness_score": 0.9,
            "relevancy_score": 0.95
        },
        {
            "test_case_id": 2,
            "model_name": "mistral:7b",
            "model_type": "ollama",
            "response_text": "4",
            "correctness_score": 0.8,
            "relevancy_score": 0.85
        }
    ]
    data_manager.save_test_cases(test_cases)
    data_manager.save_evaluation_results(results)
    stats = data_manager.get_summary_statistics()
    
    assert stats["total_evaluations"] == 2
    assert stats["total_test_cases"] == 2
    assert set(stats["models_evaluated"]) == {"llama3:8b", "mistral:7b"}
    assert stats["average_scores"]["llama3:8b"]["correctness_score"] == 0.9
    assert stats["average_scores"]["mistral:7b"]["correctness_score"] == 0.8
    assert stats["pass_rates"]["correctness_score"] == 100.0  # Both 0.9, 0.8 >= 0.7
    assert stats["pass_rates"]["relevancy_score"] == 100.0  # Both 0.95, 0.85 >= 0.8
    assert stats["category_counts"] == {"greeting": 1, "math": 1}

def test_get_summary_statistics_empty(data_manager, mocker):
    """Test summary statistics with no evaluation results."""
    mock_config = mocker.patch("src.utils.config.Config")
    mock_config_instance = mock_config.return_value
    mock_config_instance.get_available_metrics.return_value = {}
    mock_config_instance.metrics_config = {"thresholds": {}}
    
    test_cases = [
        {"id": 1, "input_text": "Hello", "expected_output": "Hi", "category": "greeting"}
    ]
    data_manager.save_test_cases(test_cases)
    stats = data_manager.get_summary_statistics()
    
    assert stats["total_evaluations"] == 0
    assert stats["total_test_cases"] == 1
    assert stats["models_evaluated"] == []
    assert stats["average_scores"] == {}
    assert stats["pass_rates"] == {}
    assert stats["category_counts"] == {"greeting": 1}