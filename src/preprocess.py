import pandas as pd
import numpy as np


def preprocess_product_information(df):
    """
    Preprocess Product_Information sheet.
    
    Steps:
    - Trim column names
    - Convert Launch_Date to datetime
    - Remove duplicates
    - Standardize text columns
    - Validate MSRP and Wholesale_Price as numeric
    """
    df = df.copy()
    
    # Trim column names
    df.columns = df.columns.str.strip()
    
    # Convert Launch_Date to datetime
    if 'Launch_Date' in df.columns:
        df['Launch_Date'] = pd.to_datetime(df['Launch_Date'], errors='coerce')
    
    # Remove duplicates
    initial_rows = len(df)
    df = df.drop_duplicates()
    removed_duplicates = initial_rows - len(df)
    print(f"Removed {removed_duplicates} duplicate rows from Product_Information")
    
    # Standardize text columns
    text_columns = df.select_dtypes(include='object').columns
    for col in text_columns:
        if col != 'Launch_Date':  # Skip datetime columns
            df[col] = df[col].str.strip().str.lower()
    
    # Validate MSRP and Wholesale_Price as numeric
    numeric_cols = ['MSRP', 'Wholesale_Price']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            missing_count = df[col].isnull().sum()
            if missing_count > 0:
                print(f"Warning: {missing_count} non-numeric values in {col}, converted to NaN")
    
    return df


def preprocess_weekly_sales(df):
    """
    Preprocess Weekly_Sales sheet.
    
    Steps:
    - Convert Week_End_Date to datetime
    - Remove duplicates
    - Validate Product_ID + Week_End_Date uniqueness
    - Numeric conversion for Qty_Sold, Inventory, On_Order, Returns, Discount
    - Sort by Product_ID and Week_End_Date
    """
    df = df.copy()
    
    # Trim column names
    df.columns = df.columns.str.strip()
    
    # Convert Week_End_Date to datetime
    if 'Week_End_Date' in df.columns:
        df['Week_End_Date'] = pd.to_datetime(df['Week_End_Date'], errors='coerce')
    
    # Remove duplicates
    initial_rows = len(df)
    df = df.drop_duplicates()
    removed_duplicates = initial_rows - len(df)
    print(f"Removed {removed_duplicates} duplicate rows from Weekly_Sales")
    
    # Numeric conversion for key columns
    numeric_cols = ['Qty_Sold', 'Inventory', 'On_Order', 'Returns', 'Discount']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            missing_count = df[col].isnull().sum()
            if missing_count > 0:
                print(f"Warning: {missing_count} non-numeric values in {col}, converted to NaN")
    
    # Validate Product_ID + Week_End_Date uniqueness
    if 'Product_ID' in df.columns and 'Week_End_Date' in df.columns:
        unique_pairs = df.groupby(['Product_ID', 'Week_End_Date']).size()
        duplicates_count = (unique_pairs > 1).sum()
        if duplicates_count > 0:
            print(f"Warning: {duplicates_count} duplicate Product_ID + Week_End_Date combinations found")
    
    # Sort by Product_ID and Week_End_Date
    if 'Product_ID' in df.columns and 'Week_End_Date' in df.columns:
        df = df.sort_values(by=['Product_ID', 'Week_End_Date']).reset_index(drop=True)
    
    return df


def preprocess_external_features(df):
    """
    Preprocess External_Features sheet.
    
    Steps:
    - Convert Week_End_Date to datetime
    - Numeric conversion for Rainfall, Avg_Temperature
    - Validate Holiday and Promo_Event as numeric/binary
    - Standardize Season text
    - Remove duplicates
    """
    df = df.copy()
    
    # Trim column names
    df.columns = df.columns.str.strip()
    
    # Convert Week_End_Date to datetime
    if 'Week_End_Date' in df.columns:
        df['Week_End_Date'] = pd.to_datetime(df['Week_End_Date'], errors='coerce')
    
    # Numeric conversion for Rainfall and Avg_Temperature
    numeric_cols = ['Rainfall', 'Avg_Temperature']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            missing_count = df[col].isnull().sum()
            if missing_count > 0:
                print(f"Warning: {missing_count} non-numeric values in {col}, converted to NaN")
    
    # Validate Holiday and Promo_Event as numeric/binary
    binary_cols = ['Holiday', 'Promo_Event']
    for col in binary_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            # Check if values are binary (0 or 1)
            unique_vals = df[col].dropna().unique()
            non_binary = set(unique_vals) - {0, 1}
            if non_binary:
                print(f"Warning: {col} contains non-binary values: {non_binary}")
    
    # Standardize Season text
    if 'Season' in df.columns:
        df['Season'] = df['Season'].str.strip().str.lower()
    
    # Remove duplicates
    initial_rows = len(df)
    df = df.drop_duplicates()
    removed_duplicates = initial_rows - len(df)
    print(f"Removed {removed_duplicates} duplicate rows from External_Features")
    
    return df
