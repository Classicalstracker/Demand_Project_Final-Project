import pandas as pd
from .config import DATA_RAW

def load_product_information():
    """
    Load Product_Information sheet from the Excel dataset.
    """
    file_path = DATA_RAW / "trail_edge_dataset.xlsx"
    df = pd.read_excel(file_path, sheet_name='Product_Information')
    # Parse date columns if present
    date_columns = [col for col in df.columns if 'date' in col.lower() or 'time' in col.lower()]
    for col in date_columns:
        df[col] = pd.to_datetime(df[col], errors='coerce')
    return df

def load_weekly_sales():
    """
    Load Weekly_Sales sheet from the Excel dataset.
    """
    file_path = DATA_RAW / "trail_edge_dataset.xlsx"
    df = pd.read_excel(file_path, sheet_name='Weekly_Sales')
    # Parse date columns if present
    date_columns = [col for col in df.columns if 'date' in col.lower() or 'time' in col.lower() or 'week' in col.lower()]
    for col in date_columns:
        df[col] = pd.to_datetime(df[col], errors='coerce')
    return df

def load_external_features():
    """
    Load External_Features sheet from the Excel dataset.
    """
    file_path = DATA_RAW / "trail_edge_dataset.xlsx"
    df = pd.read_excel(file_path, sheet_name='External_Features')
    # Parse date columns if present
    date_columns = [col for col in df.columns if 'date' in col.lower() or 'time' in col.lower()]
    for col in date_columns:
        df[col] = pd.to_datetime(df[col], errors='coerce')
    return df