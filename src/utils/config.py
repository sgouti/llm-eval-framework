import os
import yaml
from pathlib import Path
from typing import Dict, Any, List
import streamlit as st

class Config:
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self.models_config_path = self.config_dir / "models_config.yaml"
        self.metrics_config_path = self.config_dir / "metrics_config.yaml"
        self.config_dir.mkdir(exist_ok=True)
        self.models_config = self._load_models_config()
        self.metrics_config = self._load_metrics_config()

    def _load_models_config(self) -> Dict[str, Any]:
        default_config = {
            'ollama': {
                'base_url': 'http://localhost:11434',
                'timeout': 60,
                'models': [
                    'llama3.1:latest ',
                    'llama3:8b', 'llama3:70b', 'llama2:7b', 'llama2:13b', 'llama2:70b',
                    'mistral:7b', 'mistral:instruct', 'mixtral:8x7b', 'mixtral:8x22b',
                    'codellama:7b', 'codellama:13b', 'codellama:34b',
                    'phi3:mini', 'phi3:medium', 'gemma:2b', 'gemma:7b',
                    'qwen:4b', 'qwen:7b', 'qwen:14b', 'vicuna:7b', 'vicuna:13b',
                    'orca-mini:3b', 'orca-mini:7b', 'neural-chat:7b',
                    'starling-lm:7b', 'openchat:7b', 'zephyr:7b-beta'
                ]
            },
            'bedrock': {
                'region': 'us-east-1',
                'timeout': 60,
                'models': [
                    'anthropic.claude-v2',
                    'anthropic.claude-v2:1',
                    'anthropic.claude-instant-v1',
                    'amazon.titan-text-express-v1',
                    'amazon.titan-text-lite-v1',
                    'meta.llama2-13b-chat-v1',
                    'meta.llama2-70b-chat-v1'
                ]
            }
        }
        if self.models_config_path.exists():
            try:
                with open(self.models_config_path, 'r') as f:
                    config = yaml.safe_load(f)
                    for key, value in default_config.items():
                        if key not in config:
                            config[key] = value
                    return config
            except Exception as e:
                st.warning(f"Error loading models config: {e}. Using defaults.")
                return default_config
        else:
            self._save_models_config(default_config)
            return default_config

    def _load_metrics_config(self) -> Dict[str, Any]:
        default_config = {
            'default_metrics': [
                'correctness', 'relevancy', 'fluency', 'coherence'
            ],
            'available_metrics': {
                'correctness': {
                    'name': 'Correctness',
                    'description': 'Measures factual accuracy of the response',
                    'scale': '0-1',
                    'higher_is_better': True
                },
                'relevancy': {
                    'name': 'Relevancy',
                    'description': 'Measures how relevant the response is to the input',
                    'scale': '0-1',
                    'higher_is_better': True
                },
                'fluency': {
                    'name': 'Fluency',
                    'description': 'Measures linguistic fluency and readability',
                    'scale': '0-1',
                    'higher_is_better': True
                },
                'coherence': {
                    'name': 'Coherence',
                    'description': 'Measures logical consistency and coherence',
                    'scale': '0-1',
                    'higher_is_better': True
                },
                'toxicity': {
                    'name': 'Toxicity',
                    'description': 'Detects toxic or harmful content',
                    'scale': '0-1',
                    'higher_is_better': False
                },
                'bias': {
                    'name': 'Bias Detection',
                    'description': 'Detects potential bias in responses',
                    'scale': '0-1',
                    'higher_is_better': False
                }
            },
            'thresholds': {
                'correctness': 0.7,
                'relevancy': 0.8,
                'fluency': 0.7,
                'coherence': 0.7,
                'toxicity': 0.2,
                'bias': 0.3
            }
        }
        if self.metrics_config_path.exists():
            try:
                with open(self.metrics_config_path, 'r') as f:
                    return yaml.safe_load(f)
            except Exception as e:
                st.warning(f"Error loading metrics config: {e}. Using defaults.")
                return default_config
        else:
            self._save_metrics_config(default_config)
            return default_config

    def _save_models_config(self, config: Dict[str, Any]):
        with open(self.models_config_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)

    def _save_metrics_config(self, config: Dict[str, Any]):
        with open(self.metrics_config_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)

    def get_available_ollama_models(self) -> List[str]:
        return self.models_config.get('ollama', {}).get('models', [])

    def get_available_bedrock_models(self) -> List[str]:
        return self.models_config.get('bedrock', {}).get('models', [])

    def get_available_openai_models(self) -> List[str]:
        return self.models_config.get('openai', {}).get('models', [])

    def get_available_metrics(self) -> Dict[str, Any]:
        return self.metrics_config.get('available_metrics', {})

    def get_default_metrics(self) -> List[str]:
        return self.metrics_config.get('default_metrics', [])

    def get_metric_threshold(self, metric_name: str) -> float:
        return self.metrics_config.get('thresholds', {}).get(metric_name, 0.5)

    def update_models_config(self, new_config: Dict[str, Any]):
        self.models_config.update(new_config)
        self._save_models_config(self.models_config)

    def update_metrics_config(self, new_config: Dict[str, Any]):
        self.metrics_config.update(new_config)
        self._save_metrics_config(self.metrics_config)

    @property
    def data_dir(self) -> Path:
        return Path("data")

    @property
    def reports_dir(self) -> Path:
        return Path("reports")

    @property
    def logs_dir(self) -> Path:
        return Path("logs")