import pandas as pd

def generate_report(results_df):
    if results_df.empty:
        return "No results to report"
    numeric_cols = [col for col in results_df.columns if col.endswith('_score') and pd.api.types.is_numeric_dtype(results_df[col])]
    if not numeric_cols:
        return "No score columns found"
    summary = results_df.groupby('model_name')[numeric_cols].mean().reset_index()
    return summary.to_dict(orient='records')