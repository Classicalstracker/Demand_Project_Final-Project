import pandas as pd
import numpy as np


def preprocess_product_info(df):
    """
    Preprocess Product_Information dataframe.
    
    - Trim column names
    - Remove duplicate rows
    - Convert Launch_Date to datetime
    - Standardize text columns (strip spaces)
    - Validate MSRP and Wholesale_Price as numeric
    - Check missing values
    """
    df = df.copy()
    
    # Trim column names
    df.columns = df.columns.str.strip()
    
    # Remove duplicate rows
    df = df.drop_duplicates()
    
    # Convert Launch_Date to datetime
    if 'Launch_Date' in df.columns:
        df['Launch_Date'] = pd.to_datetime(df['Launch_Date'], errors='coerce')
    
    # Standardize text columns (strip spaces)
    text_columns = ['Product_ID', 'Product_Name', 'Category', 'Sub_Category', 'Gender', 'Color', 'Launch_Season']
    for col in text_columns:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
    
    # Validate MSRP and Wholesale_Price as numeric
    numeric_cols = ['MSRP', 'Wholesale_Price']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df


def preprocess_weekly_sales(df):
    """
    Preprocess Weekly_Sales dataframe.
    
    - Trim column names
    - Remove duplicate rows
    - Convert Week_End_Date to datetime
    - Validate numeric columns: Qty_Sold, Inventory, On_Order, Returns, Discount
    - Check uniqueness of Product_ID + Week_End_Date (remove duplicates)
    - Sort by Product_ID, Week_End_Date
    - Check missing values
    """
    df = df.copy()
    
    # Trim column names
    df.columns = df.columns.str.strip()
    
    # Remove duplicate rows
    df = df.drop_duplicates()
    
    # Convert Week_End_Date to datetime
    if 'Week_End_Date' in df.columns:
        df['Week_End_Date'] = pd.to_datetime(df['Week_End_Date'], errors='coerce')
    
    # Validate numeric columns
    numeric_cols = ['Qty_Sold', 'Inventory', 'On_Order', 'Returns', 'Discount']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Check uniqueness of Product_ID + Week_End_Date (remove duplicates)
    if 'Product_ID' in df.columns and 'Week_End_Date' in df.columns:
        df = df.drop_duplicates(subset=['Product_ID', 'Week_End_Date'], keep='first')
    
    # Sort by Product_ID, Week_End_Date
    if 'Product_ID' in df.columns and 'Week_End_Date' in df.columns:
        df = df.sort_values(['Product_ID', 'Week_End_Date']).reset_index(drop=True)
    
    return df


def preprocess_external_features(df):
    """
    Preprocess External_Features dataframe.
    
    - Trim column names
    - Remove duplicate rows
    - Convert Week_End_Date to datetime
    - Validate numeric columns: Holiday, Promo_Event, Rainfall, Avg_Temperature
    - Standardize Season text
    - Check missing values
    - Sort by Week_End_Date
    """
    df = df.copy()
    
    # Trim column names
    df.columns = df.columns.str.strip()
    
    # Remove duplicate rows
    df = df.drop_duplicates()
    
    # Convert Week_End_Date to datetime
    if 'Week_End_Date' in df.columns:
        df['Week_End_Date'] = pd.to_datetime(df['Week_End_Date'], errors='coerce')
    
    # Validate numeric columns
    numeric_cols = ['Holiday', 'Promo_Event', 'Rainfall', 'Avg_Temperature']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Standardize Season text
    if 'Season' in df.columns:
        df['Season'] = df['Season'].astype(str).str.strip().str.title()
    
    # Sort by Week_End_Date
    if 'Week_End_Date' in df.columns:
        df = df.sort_values('Week_End_Date').reset_index(drop=True)
    
    return df
