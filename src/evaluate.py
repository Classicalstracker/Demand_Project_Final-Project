"""
Model Evaluation Module

This module provides evaluation metrics and functions for time series forecasting models.

Metrics:
- MAE (Mean Absolute Error)
- RMSE (Root Mean Squared Error)
- MAPE (Mean Absolute Percentage Error) - safe version
- WAPE (Weighted Absolute Percentage Error)
- R² (Coefficient of Determination)
"""

import numpy as np
import pandas as pd
from pathlib import Path
from typing import Tuple, Dict


def safe_mape(y_true: np.ndarray, y_pred: np.ndarray, epsilon: float = 1e-10) -> float:
    """
    Calculate Mean Absolute Percentage Error (safe version).
    
    Handles zero values in y_true by adding small epsilon.
    
    Parameters:
    - y_true: Actual values
    - y_pred: Predicted values
    - epsilon: Small value to avoid division by zero
    
    Returns:
    - MAPE value as percentage
    """
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    
    # Avoid division by zero
    denominator = np.maximum(np.abs(y_true), epsilon)
    mape = np.mean(np.abs((y_true - y_pred) / denominator)) * 100
    
    return float(mape)


def wape(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    Calculate Weighted Absolute Percentage Error.
    
    WAPE = sum(|y_true - y_pred|) / sum(|y_true|) * 100
    
    Parameters:
    - y_true: Actual values
    - y_pred: Predicted values
    
    Returns:
    - WAPE value as percentage
    """
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    
    numerator = np.sum(np.abs(y_true - y_pred))
    denominator = np.sum(np.abs(y_true))
    
    if denominator == 0:
        return 0.0
    
    return float((numerator / denominator) * 100)


def mae(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    Calculate Mean Absolute Error.
    
    Parameters:
    - y_true: Actual values
    - y_pred: Predicted values
    
    Returns:
    - MAE value
    """
    return float(np.mean(np.abs(y_true - y_pred)))


def rmse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    Calculate Root Mean Squared Error.
    
    Parameters:
    - y_true: Actual values
    - y_pred: Predicted values
    
    Returns:
    - RMSE value
    """
    mse = np.mean((y_true - y_pred) ** 2)
    return float(np.sqrt(mse))


def r_squared(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    Calculate R² (Coefficient of Determination).
    
    Parameters:
    - y_true: Actual values
    - y_pred: Predicted values
    
    Returns:
    - R² value (0 to 1, higher is better)
    """
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    
    if ss_tot == 0:
        return 0.0
    
    return float(1 - (ss_res / ss_tot))


def evaluate_model(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    """
    Calculate all evaluation metrics.
    
    Parameters:
    - y_true: Actual values
    - y_pred: Predicted values
    
    Returns:
    - Dictionary with all metrics
    """
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    
    metrics = {
        'MAE': mae(y_true, y_pred),
        'RMSE': rmse(y_true, y_pred),
        'MAPE': safe_mape(y_true, y_pred),
        'WAPE': wape(y_true, y_pred),
        'R2': r_squared(y_true, y_pred)
    }
    
    return metrics


def compare_models(results: Dict[str, Dict[str, float]]) -> pd.DataFrame:
    """
    Create comparison DataFrame from multiple model results.
    
    Parameters:
    - results: Dictionary mapping model names to metric dictionaries
    
    Returns:
    - DataFrame with models as rows and metrics as columns
    """
    df_results = pd.DataFrame(results).T
    
    # Sort by RMSE (ascending, lower is better)
    df_results = df_results.sort_values('RMSE')
    
    return df_results


def get_feature_importance(model, feature_names: list) -> pd.DataFrame:
    """
    Extract feature importance from tree-based models.
    
    Parameters:
    - model: Fitted model with feature_importances_ attribute
    - feature_names: List of feature names
    
    Returns:
    - DataFrame with features and importances, sorted descending
    """
    if not hasattr(model, 'feature_importances_'):
        return None
    
    importances = model.feature_importances_
    
    df_importance = pd.DataFrame({
        'Feature': feature_names,
        'Importance': importances
    }).sort_values('Importance', ascending=False)
    
    return df_importance


def save_metrics_to_excel(metrics_dict: Dict[str, Dict], 
                         file_path: Path,
                         sheet_name: str = 'Metrics') -> None:
    """
    Save model metrics to Excel file.
    
    Parameters:
    - metrics_dict: Dictionary with model names and their metrics
    - file_path: Path to save Excel file
    - sheet_name: Sheet name in Excel
    """
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Convert to DataFrame
    df_metrics = pd.DataFrame(metrics_dict).T
    
    # Save to Excel
    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        df_metrics.to_excel(writer, sheet_name=sheet_name, index=True)


def save_feature_importance(importance_df: pd.DataFrame, file_path: Path) -> None:
    """
    Save feature importance to CSV.
    
    Parameters:
    - importance_df: DataFrame with feature importances
    - file_path: Path to save CSV
    """
    file_path.parent.mkdir(parents=True, exist_ok=True)
    importance_df.to_csv(file_path, index=False)
