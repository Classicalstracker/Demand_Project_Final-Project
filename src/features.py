"""
Feature Engineering Module

This module provides functions to create comprehensive model-ready features
for weekly demand forecasting.

Features include:
- Date features from Week_End_Date
- Lag features per Product_ID
- Rolling features per Product_ID
- Business features
- External features
- Demand classification features
"""

import pandas as pd
import numpy as np
from pathlib import Path


def merge_inputs(merged_df, classification_df):
    """
    Merge merged_dataset with demand_classification on Product_ID.
    
    Parameters:
    - merged_df: DataFrame from merged_dataset.csv
    - classification_df: DataFrame from demand_classification.csv
    
    Returns:
    - Merged DataFrame with demand class labels
    """
    df = merged_df.merge(
        classification_df[['Product_ID', 'Demand_Class']],
        on='Product_ID',
        how='left'
    )
    return df


def create_date_features(df, date_col='Week_End_Date'):
    """
    Create date-based features from Week_End_Date.
    
    Features:
    - Year
    - Month
    - Quarter
    - ISO_Week
    - Week_Number
    - Month_Start (first day of month as date)
    - Month_End (last day of month as date)
    
    Parameters:
    - df: DataFrame with date column
    - date_col: Name of date column
    
    Returns:
    - DataFrame with new date features
    """
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    
    df['Year'] = df[date_col].dt.year
    df['Month'] = df[date_col].dt.month
    df['Quarter'] = df[date_col].dt.quarter
    df['ISO_Week'] = df[date_col].dt.isocalendar().week
    df['Week_Number'] = df[date_col].dt.strftime('%U').astype(int)
    df['Month_Start'] = df[date_col].dt.to_period('M').apply(lambda r: r.start_time)
    df['Month_End'] = df[date_col].dt.to_period('M').apply(lambda r: r.end_time)
    
    return df


def create_lag_features(df, target_col='Qty_Sold', group_col='Product_ID', lags=[1, 2, 3, 4, 8, 12]):
    """
    Create lag features for each Product_ID.
    Uses shift to prevent target leakage.
    
    Parameters:
    - df: DataFrame (must be sorted by Product_ID and Week_End_Date)
    - target_col: Name of target column to lag
    - group_col: Column to group by (typically Product_ID)
    - lags: List of lag periods to create
    
    Returns:
    - DataFrame with lag features
    """
    df = df.copy()
    
    for lag in lags:
        col_name = f'Lag_{lag}'
        df[col_name] = df.groupby(group_col)[target_col].shift(lag)
    
    return df


def create_rolling_features(df, target_col='Qty_Sold', group_col='Product_ID', windows=[4, 8]):
    """
    Create rolling features per Product_ID.
    Uses shifted data to prevent target leakage (past data only).
    
    Features:
    - Rolling_Mean_4, Rolling_Mean_8
    - Rolling_Std_4
    - Rolling_Max_4
    - Rolling_Min_4
    
    Parameters:
    - df: DataFrame (must be sorted by Product_ID and Week_End_Date)
    - target_col: Name of target column for rolling stats
    - group_col: Column to group by
    - windows: List of window sizes for rolling calculations
    
    Returns:
    - DataFrame with rolling features
    """
    df = df.copy()
    
    for window in windows:
        shifted_target = df.groupby(group_col)[target_col].shift(1)
        rolling = shifted_target.groupby(df[group_col]).rolling(
            window=window,
            min_periods=1
        )

        # Rolling mean
        df[f'Rolling_Mean_{window}'] = rolling.mean().reset_index(level=0, drop=True)
        
        # Rolling std (only for window 4)
        if window == 4:
            df[f'Rolling_Std_{window}'] = rolling.std().reset_index(level=0, drop=True)
            
            # Rolling max and min (only for window 4)
            df[f'Rolling_Max_{window}'] = rolling.max().reset_index(level=0, drop=True)
            
            df[f'Rolling_Min_{window}'] = rolling.min().reset_index(level=0, drop=True)
    
    return df


def create_business_features(df):
    """
    Create business-relevant features from existing columns.
    
    Features:
    - Discount_Flag: 1 if Discount > 0, else 0
    - Returns_Rate: Returns / Qty_Sold (handle division by zero)
    - Inventory_Ratio: Inventory / Qty_Sold (handle division by zero)
    - Promo_Flag: 1 if Promo_Event = 1, else 0
    - Holiday_Flag: 1 if Holiday = 1, else 0
    
    Parameters:
    - df: DataFrame with required columns
    
    Returns:
    - DataFrame with business features
    """
    df = df.copy()
    
    # Discount flag
    df['Discount_Flag'] = (df['Discount'] > 0).astype(int)
    
    # Returns rate (handle division by zero)
    df['Returns_Rate'] = np.where(
        df['Qty_Sold'] > 0,
        df['Returns'] / df['Qty_Sold'],
        0
    )
    
    # Inventory ratio (handle division by zero)
    df['Inventory_Ratio'] = np.where(
        df['Qty_Sold'] > 0,
        df['Inventory'] / df['Qty_Sold'],
        0
    )
    
    # Promo flag
    df['Promo_Flag'] = df['Promo_Event'].astype(int)
    
    # Holiday flag
    df['Holiday_Flag'] = df['Holiday'].astype(int)
    
    return df


def select_features(df):
    """
    Select final set of features for modeling.
    Excludes raw data columns that are now represented as features.
    
    Parameters:
    - df: DataFrame with all features
    
    Returns:
    - DataFrame with selected features only
    """
    target = 'Qty_Sold'
    
    date_features = [
        'Year', 'Month', 'Quarter', 'ISO_Week', 'Week_Number',
        'Month_Start', 'Month_End'
    ]
    
    lag_features = [f'Lag_{lag}' for lag in [1, 2, 3, 4, 8, 12]]
    
    rolling_features = [
        'Rolling_Mean_4', 'Rolling_Mean_8', 'Rolling_Std_4',
        'Rolling_Max_4', 'Rolling_Min_4'
    ]
    
    business_features = [
        'Discount_Flag', 'Returns_Rate', 'Inventory_Ratio',
        'Promo_Flag', 'Holiday_Flag'
    ]
    
    external_features = ['Rainfall', 'Avg_Temperature', 'Season']
    
    demand_features = ['Demand_Class']
    
    product_features = ['Product_ID']
    
    metadata_cols = ['Week_End_Date']
    
    selected_cols = (
        [target] +
        metadata_cols +
        product_features +
        date_features +
        lag_features +
        rolling_features +
        business_features +
        external_features +
        demand_features
    )
    
    # Keep only columns that exist
    selected_cols = [col for col in selected_cols if col in df.columns]
    
    return df[selected_cols]


def build_features(merged_df, classification_df):
    """
    Complete feature engineering pipeline.
    
    Parameters:
    - merged_df: merged_dataset.csv as DataFrame
    - classification_df: demand_classification.csv as DataFrame
    
    Returns:
    - Feature-ready DataFrame with all engineered features
    """
    # Step 1: Merge inputs
    df = merge_inputs(merged_df, classification_df)
    
    # Step 2: Sort by Product_ID and date (required for lag/rolling)
    df['Week_End_Date'] = pd.to_datetime(df['Week_End_Date'])
    df = df.sort_values(['Product_ID', 'Week_End_Date']).reset_index(drop=True)
    
    # Step 3: Create date features
    df = create_date_features(df)
    
    # Step 4: Create lag features
    df = create_lag_features(df)
    
    # Step 5: Create rolling features
    df = create_rolling_features(df)
    
    # Step 6: Create business features
    df = create_business_features(df)
    
    # Step 7: Select final feature set
    df = select_features(df)
    
    return df
