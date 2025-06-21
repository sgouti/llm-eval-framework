import pandas as pd
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import json
import streamlit as st
from src.utils.config import Config

class CSVDataManager:
    """Manages CSV data operations for test cases and evaluation results"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # Define file paths
        self.test_cases_file = self.data_dir / "test_cases.csv"
        self.results_file = self.data_dir / "evaluation_results.csv"
        self.models_usage_file = self.data_dir / "models_usage.csv"
        
        # Initialize CSV files if they don't exist
        self._initialize_csv_files()
    
    def _initialize_csv_files(self):
        """Initialize CSV files with proper headers if they don't exist"""
        
        # Test cases CSV structure
        if not self.test_cases_file.exists():
            test_cases_df = pd.DataFrame(columns=[
                'id', 'input_text', 'expected_output', 'context', 
                'category', 'tags', 'created_at', 'updated_at'
            ])
            test_cases_df.to_csv(self.test_cases_file, index=False)
        
        # Evaluation results CSV structure
        if not self.results_file.exists():
            results_df = pd.DataFrame(columns=[
                'id', 'test_case_id', 'model_name', 'model_type', 'response_text',
                'correctness_score', 'relevancy_score', 'fluency_score', 'coherence_score',
                'toxicity_score', 'bias_score', 'custom_metrics', 'evaluation_time',
                'duration_ms', 'status', 'error_message'
            ])
            results_df.to_csv(self.results_file, index=False)
        
        # Models usage tracking
        if not self.models_usage_file.exists():
            usage_df = pd.DataFrame(columns=[
                'model_name', 'model_type', 'total_requests', 'successful_requests',
                'failed_requests', 'avg_response_time', 'last_used'
            ])
            usage_df.to_csv(self.models_usage_file, index=False)
    
    def save_test_cases(self, test_cases: List[Dict[str, Any]]) -> bool:
        """Save test cases to CSV"""
        try:
            df = pd.DataFrame(test_cases)
            
            # Add timestamps
            current_time = datetime.now().isoformat()
            if 'created_at' not in df.columns:
                df['created_at'] = current_time
            df['updated_at'] = current_time
            
            # Generate IDs if not present
            if 'id' not in df.columns or df['id'].isna().any():
                df['id'] = range(1, len(df) + 1)
            
            # Save to CSV
            df.to_csv(self.test_cases_file, index=False)
            return True
            
        except Exception as e:
            st.error(f"Error saving test cases: {str(e)}")
            return False
    
    def load_test_cases(self, filter_conditions: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
        """Load test cases from CSV with optional filtering"""
        try:
            if not self.test_cases_file.exists():
                return pd.DataFrame(columns=[
                    'id', 'input_text', 'expected_output', 'context', 
                    'category', 'tags', 'created_at', 'updated_at'
                ])
            
            df = pd.read_csv(self.test_cases_file)
            
            # Apply filters if provided
            if filter_conditions:
                for column, value in filter_conditions.items():
                    if column in df.columns:
                        if isinstance(value, list):
                            df = df[df[column].isin(value)]
                        else:
                            df = df[df[column] == value]
            
            return df
            
        except Exception as e:
            st.error(f"Error loading test cases: {str(e)}")
            return pd.DataFrame()
    
    def add_test_case(self, test_case: Dict[str, Any]) -> bool:
        """Add a single test case"""
        try:
            existing_df = self.load_test_cases()
            
            # Generate new ID
            if len(existing_df) > 0:
                new_id = existing_df['id'].max() + 1
            else:
                new_id = 1
            
            test_case['id'] = new_id
            test_case['created_at'] = datetime.now().isoformat()
            test_case['updated_at'] = datetime.now().isoformat()
            
            # Append to existing data
            new_row = pd.DataFrame([test_case])
            updated_df = pd.concat([existing_df, new_row], ignore_index=True)
            
            updated_df.to_csv(self.test_cases_file, index=False)
            return True
            
        except Exception as e:
            st.error(f"Error adding test case: {str(e)}")
            return False
    
    def save_evaluation_results(self, results: List[Dict[str, Any]]) -> bool:
        """Save evaluation results to CSV"""
        try:
            new_results_df = pd.DataFrame(results)
            
            # Load existing results
            if self.results_file.exists():
                existing_df = pd.read_csv(self.results_file)
                
                # Generate new IDs
                if len(existing_df) > 0:
                    start_id = existing_df['id'].max() + 1
                else:
                    start_id = 1
                
                new_results_df['id'] = range(start_id, start_id + len(new_results_df))
                
                # Combine with existing data
                combined_df = pd.concat([existing_df, new_results_df], ignore_index=True)
            else:
                new_results_df['id'] = range(1, len(new_results_df) + 1)
                combined_df = new_results_df
            
            # Save to CSV
            combined_df.to_csv(self.results_file, index=False)
            return True
            
        except Exception as e:
            st.error(f"Error saving evaluation results: {str(e)}")
            return False
    
    def load_evaluation_results(self, filter_conditions: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
        """Load evaluation results from CSV with optional filtering"""
        try:
            if not self.results_file.exists():
                return pd.DataFrame(columns=[
                    'id', 'test_case_id', 'model_name', 'model_type', 'response_text',
                    'correctness_score', 'relevancy_score', 'fluency_score', 'coherence_score',
                    'toxicity_score', 'bias_score', 'custom_metrics', 'evaluation_time',
                    'duration_ms', 'status', 'error_message'
                ])
            
            df = pd.read_csv(self.results_file)
            
            # Apply filters if provided
            if filter_conditions:
                for column, value in filter_conditions.items():
                    if column in df.columns:
                        if isinstance(value, list):
                            df = df[df[column].isin(value)]
                        else:
                            df = df[df[column] == value]
            
            return df
            
        except Exception as e:
            st.error(f"Error loading evaluation results: {str(e)}")
            return pd.DataFrame()
    
    def get_test_case_by_id(self, test_case_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific test case by ID"""
        try:
            df = self.load_test_cases()
            filtered_df = df[df['id'] == test_case_id]
            
            if len(filtered_df) > 0:
                return filtered_df.iloc[0].to_dict()
            return None
            
        except Exception as e:
            st.error(f"Error getting test case by ID: {str(e)}")
            return None
    
    def get_results_by_model(self, model_name: str) -> pd.DataFrame:
        """Get evaluation results for a specific model"""
        return self.load_evaluation_results({'model_name': model_name})
    
    def get_results_by_category(self, category: str) -> pd.DataFrame:
        """Get evaluation results for a specific category"""
        try:
            results_df = self.load_evaluation_results()
            test_cases_df = self.load_test_cases()
            
            # Filter test cases by category
            category_test_cases = test_cases_df[test_cases_df['category'] == category]['id'].tolist()
            
            # Filter results by test case IDs
            filtered_results = results_df[results_df['test_case_id'].isin(category_test_cases)]
            
            return filtered_results
            
        except Exception as e:
            st.error(f"Error getting results by category: {str(e)}")
            return pd.DataFrame()

    def calculate_pass_rate(self, results_df: pd.DataFrame, metric: str, threshold: float, higher_is_better: bool = True) -> float:
        """Calculate the pass rate for a specific metric based on its threshold"""
        try:
            if metric not in results_df.columns or results_df[metric].empty:
                return 0.0
            if higher_is_better:
                pass_count = len(results_df[results_df[metric] >= threshold])
            else:
                pass_count = len(results_df[results_df[metric] <= threshold])
            total_count = len(results_df)
            return (pass_count / total_count * 100) if total_count > 0 else 0.0
        except Exception as e:
            st.error(f"Error calculating pass rate for {metric}: {str(e)}")
            return 0.0

    def get_summary_statistics(self) -> Dict[str, Any]:
        """Get summary statistics for the evaluation results"""
        try:
            results_df = self.load_evaluation_results()
            test_cases_df = self.load_test_cases()
            
            if len(results_df) == 0:
                return {
                    "total_evaluations": 0,
                    "total_test_cases": len(test_cases_df),
                    "models_evaluated": [],
                    "average_scores": {},
                    "pass_rates": {},
                    "category_counts": test_cases_df['category'].value_counts().to_dict() if not test_cases_df.empty else {}
                }

            # Initialize config for thresholds
            config = Config()
            metrics_config = config.get_available_metrics()
            thresholds = config.metrics_config.get('thresholds', {})

            # Identify numeric score columns
            score_columns = [col for col in results_df.columns if col.endswith('_score') and pd.api.types.is_numeric_dtype(results_df[col])]

            # Calculate average scores per model
            average_scores = {}
            if score_columns:
                avg_scores_df = results_df.groupby('model_name')[score_columns].mean().reset_index()
                average_scores = avg_scores_df.set_index('model_name').to_dict('index')

            # Calculate pass rates for each metric
            pass_rates = {}
            for metric in score_columns:
                metric_name = metric.replace('_score', '')
                threshold = thresholds.get(metric_name, 0.5)
                higher_is_better = metrics_config.get(metric_name, {}).get('higher_is_better', True)
                pass_rates[metric] = self.calculate_pass_rate(results_df, metric, threshold, higher_is_better)

            # Get unique models evaluated
            models_evaluated = results_df['model_name'].unique().tolist()

            # Get category counts from test cases
            category_counts = test_cases_df['category'].value_counts().to_dict() if not test_cases_df.empty else {}

            return {
                "total_evaluations": len(results_df),
                "total_test_cases": len(test_cases_df),
                "models_evaluated": models_evaluated,
                "average_scores": average_scores,
                "pass_rates": pass_rates,
                "category_counts": category_counts
            }
            
        except Exception as e:
            st.error(f"Error generating summary statistics: {str(e)}")
            return {
                "total_evaluations": 0,
                "total_test_cases": 0,
                "models_evaluated": [],
                "average_scores": {},
                "pass_rates": {},
                "category_counts": {}
            }