"""
Demand Classification Module

This module provides functions for classifying product demand patterns
using standard inventory management metrics: ADI (Average Demand Interval)
and CV² (Squared Coefficient of Variation).

Classification Rules:
- Smooth: ADI < 1.32 and CV² < 0.49
- Erratic: ADI < 1.32 and CV² >= 0.49
- Intermittent: ADI >= 1.32 and CV² < 0.49
- Lumpy: ADI >= 1.32 and CV² >= 0.49
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Set seaborn style
sns.set_style("whitegrid")

def calculate_demand_metrics(df, product_id_col='Product_ID', demand_col='Qty_Sold', time_col='Week_End_Date'):
    """
    Calculate ADI and CV² for each product.

    Parameters:
    - df: DataFrame with product demand data
    - product_id_col: Column name for product identifier
    - demand_col: Column name for demand quantity
    - time_col: Column name for time period

    Returns:
    - DataFrame with demand metrics for each product
    """
    results = []

    for product_id in df[product_id_col].unique():
        product_data = df[df[product_id_col] == product_id].copy()
        product_data = product_data.sort_values(time_col)

        demand_series = product_data[demand_col].values
        total_periods = len(demand_series)

        # Non-zero demands
        non_zero_demands = demand_series[demand_series > 0]

        if len(non_zero_demands) == 0:
            # No demand at all - special case
            adi = float('inf')
            cv_squared = 0
            mean_demand = 0
            std_demand = 0
        else:
            # ADI = Average Demand Interval = total periods / number of non-zero demand periods
            adi = total_periods / len(non_zero_demands)

            # CV² = (std/mean)² for non-zero demands
            mean_demand = np.mean(non_zero_demands)
            std_demand = np.std(non_zero_demands, ddof=1)  # Sample standard deviation

            if mean_demand == 0:
                cv_squared = 0
            else:
                cv_squared = (std_demand / mean_demand) ** 2

        results.append({
            product_id_col: product_id,
            'Total_Periods': total_periods,
            'Non_Zero_Periods': len(non_zero_demands),
            'ADI': adi,
            'Mean_Demand': mean_demand,
            'Std_Demand': std_demand,
            'CV_Squared': cv_squared
        })

    return pd.DataFrame(results)

def classify_demand_pattern(adi, cv_squared):
    """
    Classify demand pattern based on ADI and CV² thresholds.

    Parameters:
    - adi: Average Demand Interval
    - cv_squared: Squared Coefficient of Variation

    Returns:
    - demand_class: String classification
    """
    if adi < 1.32 and cv_squared < 0.49:
        return 'Smooth'
    elif adi < 1.32 and cv_squared >= 0.49:
        return 'Erratic'
    elif adi >= 1.32 and cv_squared < 0.49:
        return 'Intermittent'
    else:  # adi >= 1.32 and cv_squared >= 0.49
        return 'Lumpy'

def classify_all_products(metrics_df):
    """
    Classify all products based on their demand metrics.

    Parameters:
    - metrics_df: DataFrame with demand metrics

    Returns:
    - DataFrame with classification added
    """
    df = metrics_df.copy()
    df['Demand_Class'] = df.apply(lambda row: classify_demand_pattern(row['ADI'], row['CV_Squared']), axis=1)
    return df

def create_demand_classification_summary(classified_df):
    """
    Create summary statistics for demand classification.

    Parameters:
    - classified_df: DataFrame with classified products

    Returns:
    - summary_df: Summary statistics by demand class
    """
    summary = classified_df.groupby('Demand_Class').agg({
        'Product_ID': 'count',
        'ADI': ['mean', 'min', 'max'],
        'CV_Squared': ['mean', 'min', 'max'],
        'Mean_Demand': ['mean', 'min', 'max']
    }).round(3)

    # Flatten column names
    summary.columns = ['_'.join(col).strip() for col in summary.columns.values]
    summary = summary.rename(columns={
        'Product_ID_count': 'Product_Count',
        'ADI_mean': 'ADI_Mean',
        'ADI_min': 'ADI_Min',
        'ADI_max': 'ADI_Max',
        'CV_Squared_mean': 'CV2_Mean',
        'CV_Squared_min': 'CV2_Min',
        'CV_Squared_max': 'CV2_Max',
        'Mean_Demand_mean': 'Mean_Demand_Avg',
        'Mean_Demand_min': 'Mean_Demand_Min',
        'Mean_Demand_max': 'Mean_Demand_Max'
    })

    return summary

def plot_demand_class_pie(classified_df, output_path):
    """
    Create pie chart of demand class distribution.

    Parameters:
    - classified_df: DataFrame with classified products
    - output_path: Path to save the chart
    """
    class_counts = classified_df['Demand_Class'].value_counts()

    plt.figure(figsize=(10, 8))
    colors = ['#66c2a5', '#fc8d62', '#8da0cb', '#e78ac3']  # Colorblind-friendly palette

    plt.pie(class_counts.values, labels=class_counts.index, autopct='%1.1f%%',
            colors=colors, startangle=90, wedgeprops={'edgecolor': 'white', 'linewidth': 2})

    plt.title('Demand Pattern Classification Distribution', fontsize=16, fontweight='bold')
    plt.axis('equal')

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

def plot_demand_class_bar(classified_df, output_path):
    """
    Create bar chart of demand class distribution.

    Parameters:
    - classified_df: DataFrame with classified products
    - output_path: Path to save the chart
    """
    class_counts = classified_df['Demand_Class'].value_counts()

    plt.figure(figsize=(12, 8))
    colors = ['#66c2a5', '#fc8d62', '#8da0cb', '#e78ac3']

    bars = plt.bar(class_counts.index, class_counts.values, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)

    plt.title('Demand Pattern Classification by Product Count', fontsize=16, fontweight='bold')
    plt.xlabel('Demand Class', fontsize=14)
    plt.ylabel('Number of Products', fontsize=14)

    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{int(height)}', ha='center', va='bottom', fontsize=12, fontweight='bold')

    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

def run_demand_classification(input_file, output_dir='data/processed', charts_dir='reports/charts', tables_dir='reports/tables'):
    """
    Complete demand classification pipeline.

    Parameters:
    - input_file: Path to input CSV file
    - output_dir: Directory to save classification results
    - charts_dir: Directory to save charts
    - tables_dir: Directory to save tables

    Returns:
    - classified_df: DataFrame with classified products
    - summary_df: Summary statistics
    """
    input_path = Path(input_file)
    output_path = Path(output_dir)
    charts_path = Path(charts_dir)
    tables_path = Path(tables_dir)

    # Create directories if they don't exist
    output_path.mkdir(parents=True, exist_ok=True)
    charts_path.mkdir(parents=True, exist_ok=True)
    tables_path.mkdir(parents=True, exist_ok=True)

    # Load data
    df = pd.read_csv(input_path)

    # Calculate demand metrics
    metrics_df = calculate_demand_metrics(df)

    # Classify products
    classified_df = classify_all_products(metrics_df)

    # Create summary
    summary_df = create_demand_classification_summary(classified_df)

    # Save results
    classified_df.to_csv(output_path / 'demand_classification.csv', index=False)
    summary_df.to_csv(tables_path / 'demand_class_summary.csv', index=True)

    # Create charts
    plot_demand_class_pie(classified_df, charts_path / 'demand_class_pie.png')
    plot_demand_class_bar(classified_df, charts_path / 'demand_class_bar.png')

    print("Demand classification complete!")
    print(f"Results saved to: {output_path / 'demand_classification.csv'}")
    print(f"Summary saved to: {tables_path / 'demand_class_summary.csv'}")
    print(f"Charts saved to: {charts_path}/")

    return classified_df, summary_df