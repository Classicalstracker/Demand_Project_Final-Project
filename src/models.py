"""
Model Training and Tuning Module

This module provides model training functions including:
- Baseline models (Naive, Moving Average)
- ML models (Linear Regression, Random Forest, Gradient Boosting)
- Hyperparameter tuning with TimeSeriesSplit
- Model training orchestration
"""

import numpy as np
import pandas as pd
import pickle
from pathlib import Path
from typing import Tuple, Dict, List, Optional

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import TimeSeriesSplit, GridSearchCV
from sklearn.preprocessing import StandardScaler

try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False

try:
    import lightgbm as lgb
    LIGHTGBM_AVAILABLE = True
except ImportError:
    LIGHTGBM_AVAILABLE = False

from evaluate import evaluate_model


class BaselineForecasters:
    """Baseline forecasting models for comparison."""
    
    @staticmethod
    def naive_forecast(y_train: np.ndarray, y_test: np.ndarray) -> np.ndarray:
        """
        Naive forecast: last value is repeated for all predictions.
        
        Parameters:
        - y_train: Training data
        - y_test: Test data (determines forecast length)
        
        Returns:
        - Array of predictions
        """
        last_value = y_train[-1]
        return np.full(len(y_test), last_value)
    
    @staticmethod
    def moving_average_forecast(y_train: np.ndarray, y_test: np.ndarray, window: int = 4) -> np.ndarray:
        """
        Moving average forecast: average of last N values.
        
        Parameters:
        - y_train: Training data
        - y_test: Test data (determines forecast length)
        - window: Moving average window size
        
        Returns:
        - Array of predictions
        """
        ma_value = np.mean(y_train[-window:])
        return np.full(len(y_test), ma_value)


def prepare_timeseries_data(df: pd.DataFrame, 
                            target_col: str = 'Qty_Sold',
                            drop_cols: List[str] = None) -> Tuple[np.ndarray, np.ndarray]:
    """
    Prepare feature matrix and target vector.
    
    Removes columns with excessive NaN values and target leakage candidates.
    
    Parameters:
    - df: DataFrame with features and target
    - target_col: Name of target column
    - drop_cols: Additional columns to drop
    
    Returns:
    - X: Feature matrix (NaN-filled with 0)
    - y: Target vector
    """
    if drop_cols is None:
        drop_cols = []
    
    # Standard columns to drop
    default_drop = [
        target_col, 'Week_End_Date', 'Product_ID', 'Month_Start', 'Month_End',
        'Season', 'Demand_Class'
    ]
    drop_cols = list(set(default_drop + drop_cols))
    
    # Remove only columns that exist
    drop_cols = [col for col in drop_cols if col in df.columns]
    
    # Get target and features
    y = df[target_col].values
    X = df.drop(columns=drop_cols).values
    
    # Fill NaN with 0
    X = np.nan_to_num(X, nan=0.0)
    
    return X, y


def train_baseline_models(X_train: np.ndarray, y_train: np.ndarray,
                          X_val: np.ndarray, y_val: np.ndarray) -> Dict[str, Dict]:
    """
    Train baseline models and evaluate.
    
    Parameters:
    - X_train, y_train: Training data
    - X_val, y_val: Validation data
    
    Returns:
    - Dictionary with model names as keys and results dicts as values
    """
    results = {}
    
    # Naive Forecast
    y_pred_naive = BaselineForecasters.naive_forecast(y_train, y_val)
    results['Naive'] = {
        'model': None,
        'predictions': y_pred_naive,
        'metrics': evaluate_model(y_val, y_pred_naive)
    }
    
    # Moving Average Forecast
    y_pred_ma = BaselineForecasters.moving_average_forecast(y_train, y_val, window=4)
    results['Moving_Average'] = {
        'model': None,
        'predictions': y_pred_ma,
        'metrics': evaluate_model(y_val, y_pred_ma)
    }
    
    return results


def train_ml_models(X_train: np.ndarray, y_train: np.ndarray,
                    X_val: np.ndarray, y_val: np.ndarray) -> Dict[str, Dict]:
    """
    Train ML models without tuning.
    
    Parameters:
    - X_train, y_train: Training data
    - X_val, y_val: Validation data
    
    Returns:
    - Dictionary with model names and results
    """
    results = {}
    
    # Linear Regression
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    y_pred_lr = lr.predict(X_val)
    results['LinearRegression'] = {
        'model': lr,
        'predictions': y_pred_lr,
        'metrics': evaluate_model(y_val, y_pred_lr)
    }
    
    # Random Forest
    rf = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    rf.fit(X_train, y_train)
    y_pred_rf = rf.predict(X_val)
    results['RandomForest'] = {
        'model': rf,
        'predictions': y_pred_rf,
        'metrics': evaluate_model(y_val, y_pred_rf)
    }
    
    # Gradient Boosting
    gb = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
    gb.fit(X_train, y_train)
    y_pred_gb = gb.predict(X_val)
    results['GradientBoosting'] = {
        'model': gb,
        'predictions': y_pred_gb,
        'metrics': evaluate_model(y_val, y_pred_gb)
    }
    
    # XGBoost if available
    if XGBOOST_AVAILABLE:
        xgb_model = xgb.XGBRegressor(n_estimators=100, learning_rate=0.1, 
                                     max_depth=5, random_state=42, verbosity=0)
        xgb_model.fit(X_train, y_train)
        y_pred_xgb = xgb_model.predict(X_val)
        results['XGBoost'] = {
            'model': xgb_model,
            'predictions': y_pred_xgb,
            'metrics': evaluate_model(y_val, y_pred_xgb)
        }
    
    return results


def tune_random_forest(X_train: np.ndarray, y_train: np.ndarray,
                       X_val: np.ndarray, y_val: np.ndarray,
                       cv: int = 3) -> Tuple[RandomForestRegressor, Dict]:
    """
    Tune Random Forest hyperparameters.
    
    Parameters:
    - X_train, y_train: Training data
    - X_val, y_val: Validation data
    - cv: Number of cross-validation folds
    
    Returns:
    - Best model and results dictionary
    """
    param_grid = {
        'n_estimators': [50, 100, 200],
        'max_depth': [5, 10, 15, None],
        'min_samples_leaf': [1, 2, 4]
    }
    
    tscv = TimeSeriesSplit(n_splits=cv)
    gs = GridSearchCV(RandomForestRegressor(random_state=42, n_jobs=1),
                      param_grid, cv=tscv, scoring='neg_mean_squared_error', n_jobs=1)
    gs.fit(X_train, y_train)
    
    best_model = gs.best_estimator_
    y_pred = best_model.predict(X_val)
    
    return best_model, {
        'best_params': gs.best_params_,
        'predictions': y_pred,
        'metrics': evaluate_model(y_val, y_pred)
    }


def tune_gradient_boosting(X_train: np.ndarray, y_train: np.ndarray,
                           X_val: np.ndarray, y_val: np.ndarray,
                           cv: int = 3) -> Tuple[GradientBoostingRegressor, Dict]:
    """
    Tune Gradient Boosting hyperparameters.
    
    Parameters:
    - X_train, y_train: Training data
    - X_val, y_val: Validation data
    - cv: Number of cross-validation folds
    
    Returns:
    - Best model and results dictionary
    """
    param_grid = {
        'n_estimators': [50, 100, 200],
        'learning_rate': [0.01, 0.05, 0.1],
        'max_depth': [3, 5, 7]
    }
    
    tscv = TimeSeriesSplit(n_splits=cv)
    gs = GridSearchCV(GradientBoostingRegressor(random_state=42),
                      param_grid, cv=tscv, scoring='neg_mean_squared_error')
    gs.fit(X_train, y_train)
    
    best_model = gs.best_estimator_
    y_pred = best_model.predict(X_val)
    
    return best_model, {
        'best_params': gs.best_params_,
        'predictions': y_pred,
        'metrics': evaluate_model(y_val, y_pred)
    }


def tune_xgboost(X_train: np.ndarray, y_train: np.ndarray,
                 X_val: np.ndarray, y_val: np.ndarray,
                 cv: int = 3):
    """
    Tune XGBoost hyperparameters (if available).
    
    Parameters:
    - X_train, y_train: Training data
    - X_val, y_val: Validation data
    - cv: Number of cross-validation folds
    
    Returns:
    - Best model and results dictionary
    """
    if not XGBOOST_AVAILABLE:
        return None, {}
    
    param_grid = {
        'n_estimators': [50, 100, 200],
        'learning_rate': [0.01, 0.05, 0.1],
        'max_depth': [3, 5, 7],
        'subsample': [0.6, 0.8, 1.0]
    }
    
    tscv = TimeSeriesSplit(n_splits=cv)
    gs = GridSearchCV(xgb.XGBRegressor(random_state=42, verbosity=0),
                      param_grid, cv=tscv, scoring='neg_mean_squared_error', n_jobs=-1)
    gs.fit(X_train, y_train)
    
    best_model = gs.best_estimator_
    y_pred = best_model.predict(X_val)
    
    return best_model, {
        'best_params': gs.best_params_,
        'predictions': y_pred,
        'metrics': evaluate_model(y_val, y_pred)
    }


def save_model(model, model_path: Path) -> None:
    """
    Save model to pickle file.
    
    Parameters:
    - model: Fitted model object
    - model_path: Path to save model
    """
    model_path.parent.mkdir(parents=True, exist_ok=True)
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    
    if model_path.stat().st_size == 0:
        raise IOError(f'Model save failed, file is empty: {model_path}')


def load_model(model_path: Path):
    """
    Load model from pickle file.
    
    Parameters:
    - model_path: Path to model file
    
    Returns:
    - Loaded model object
    """
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    return model


def split_timeseries_data(df: pd.DataFrame, 
                         train_ratio: float = 0.7,
                         val_ratio: float = 0.2) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Split time series data chronologically.
    
    Parameters:
    - df: DataFrame sorted by time
    - train_ratio: Proportion for training
    - val_ratio: Proportion for validation
    
    Returns:
    - train_df, val_df, test_df
    """
    n_total = len(df)
    n_train = int(n_total * train_ratio)
    n_val = int(n_total * val_ratio)
    n_test = n_total - n_train - n_val
    
    train_df = df.iloc[:n_train]
    val_df = df.iloc[n_train:n_train + n_val]
    test_df = df.iloc[n_train + n_val:]
    
    return train_df, val_df, test_df


def train_product_model(df: pd.DataFrame, 
                       product_id: str,
                       model_type: str = 'RandomForest',
                       tune: bool = True) -> Tuple[object, Dict]:
    """
    Train a model for a specific product.
    
    Parameters:
    - df: DataFrame for the product (sorted by time)
    - product_id: Product identifier
    - model_type: Type of model ('LinearRegression', 'RandomForest', 'GradientBoosting')
    - tune: Whether to perform hyperparameter tuning
    
    Returns:
    - Best model and results dictionary
    """
    # Split data
    train_df, val_df, test_df = split_timeseries_data(df)
    
    # Prepare features
    X_train, y_train = prepare_timeseries_data(train_df)
    X_val, y_val = prepare_timeseries_data(val_df)
    
    # Train model
    if model_type == 'LinearRegression':
        model = LinearRegression()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_val)
        results = {
            'predictions': y_pred,
            'metrics': evaluate_model(y_val, y_pred)
        }
        
    elif model_type == 'RandomForest':
        if tune:
            model, results = tune_random_forest(X_train, y_train, X_val, y_val)
        else:
            rf = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
            rf.fit(X_train, y_train)
            y_pred = rf.predict(X_val)
            model = rf
            results = {
                'predictions': y_pred,
                'metrics': evaluate_model(y_val, y_pred)
            }
            
    elif model_type == 'GradientBoosting':
        if tune:
            model, results = tune_gradient_boosting(X_train, y_train, X_val, y_val)
        else:
            gb = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
            gb.fit(X_train, y_train)
            y_pred = gb.predict(X_val)
            model = gb
            results = {
                'predictions': y_pred,
                'metrics': evaluate_model(y_val, y_pred)
            }
    
    return model, results


def select_best_model(baseline_results: Dict, ml_results: Dict) -> Tuple[str, object, Dict]:
    """
    Select the best model based on RMSE.
    
    Parameters:
    - baseline_results: Results from baseline models
    - ml_results: Results from ML models
    
    Returns:
    - Best model name, model object, and results
    """
    all_results = {**baseline_results, **ml_results}
    
    # Find model with lowest RMSE
    best_model_name = min(all_results.keys(), key=lambda x: all_results[x]['metrics']['RMSE'])
    best_model = all_results[best_model_name]['model']
    best_results = all_results[best_model_name]
    
    return best_model_name, best_model, best_results


def get_feature_names(df: pd.DataFrame) -> List[str]:
    """
    Get feature names after prepare_timeseries_data processing.
    
    Parameters:
    - df: DataFrame with features
    
    Returns:
    - List of feature names
    """
    drop_cols = [
        'Qty_Sold', 'Week_End_Date', 'Product_ID', 'Month_Start', 'Month_End',
        'Season', 'Demand_Class'
    ]
    drop_cols = [col for col in drop_cols if col in df.columns]
    feature_names = df.drop(columns=drop_cols).columns.tolist()
    return feature_names
