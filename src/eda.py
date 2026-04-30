import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORTS_CHARTS = PROJECT_ROOT / 'reports' / 'charts'
REPORTS_TABLES = PROJECT_ROOT / 'reports' / 'tables'

# Ensure directories exist
REPORTS_CHARTS.mkdir(parents=True, exist_ok=True)
REPORTS_TABLES.mkdir(parents=True, exist_ok=True)

def dataset_overview(df_product, df_sales, df_external):
    """Create dataset overview summary"""
    overview = {
        'Dataset': ['Product Info', 'Weekly Sales', 'External Features'],
        'Rows': [df_product.shape[0], df_sales.shape[0], df_external.shape[0]],
        'Columns': [df_product.shape[1], df_sales.shape[1], df_external.shape[1]],
        'Date_Range': [
            f"{df_product['Launch_Date'].min()} to {df_product['Launch_Date'].max()}",
            f"{df_sales['Week_End_Date'].min()} to {df_sales['Week_End_Date'].max()}",
            f"{df_external['Week_End_Date'].min()} to {df_external['Week_End_Date'].max()}"
        ]
    }
    df_overview = pd.DataFrame(overview)
    df_overview.to_csv(REPORTS_TABLES / 'dataset_overview.csv', index=False)
    return df_overview

def summary_statistics(df_product, df_sales, df_external):
    """Generate summary statistics for numeric columns"""
    stats = {}
    
    # Product info numeric stats
    numeric_cols_product = df_product.select_dtypes(include=[np.number]).columns
    stats['Product Info'] = df_product[numeric_cols_product].describe()
    
    # Sales numeric stats
    numeric_cols_sales = df_sales.select_dtypes(include=[np.number]).columns
    stats['Weekly Sales'] = df_sales[numeric_cols_sales].describe()
    
    # External numeric stats
    numeric_cols_external = df_external.select_dtypes(include=[np.number]).columns
    stats['External Features'] = df_external[numeric_cols_external].describe()
    
    # Save to CSV
    for sheet_name, df in stats.items():
        df.to_csv(REPORTS_TABLES / f'summary_statistics_{sheet_name.lower().replace(" ", "_")}.csv')
    
    return stats

def category_distribution(df_product):
    """Plot category distribution"""
    plt.figure(figsize=(10, 6))
    ax = sns.countplot(data=df_product, y='Category', order=df_product['Category'].value_counts().index)
    plt.title('Product Distribution by Category', fontsize=14, fontweight='bold')
    plt.xlabel('Count')
    plt.ylabel('Category')
    
    # Add value labels
    for p in ax.patches:
        ax.annotate(f'{p.get_width()}', (p.get_width() + 0.1, p.get_y() + p.get_height()/2), 
                   ha='left', va='center')
    
    plt.tight_layout()
    plt.savefig(REPORTS_CHARTS / 'category_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()

def gender_distribution(df_product):
    """Plot gender distribution"""
    plt.figure(figsize=(8, 6))
    ax = sns.countplot(data=df_product, x='Gender', order=df_product['Gender'].value_counts().index)
    plt.title('Product Distribution by Gender', fontsize=14, fontweight='bold')
    plt.xlabel('Gender')
    plt.ylabel('Count')
    
    # Add value labels
    for p in ax.patches:
        ax.annotate(f'{p.get_height()}', (p.get_x() + p.get_width()/2, p.get_height() + 0.1), 
                   ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig(REPORTS_CHARTS / 'gender_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()

def price_distributions(df_product):
    """Plot MSRP and Wholesale_Price distributions"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # MSRP distribution
    sns.histplot(data=df_product, x='MSRP', ax=ax1, kde=True)
    ax1.set_title('MSRP Distribution', fontsize=14, fontweight='bold')
    ax1.set_xlabel('MSRP ($)')
    ax1.set_ylabel('Frequency')
    
    # Wholesale_Price distribution
    sns.histplot(data=df_product, x='Wholesale_Price', ax=ax2, kde=True)
    ax2.set_title('Wholesale Price Distribution', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Wholesale Price ($)')
    ax2.set_ylabel('Frequency')
    
    plt.tight_layout()
    plt.savefig(REPORTS_CHARTS / 'price_distributions.png', dpi=300, bbox_inches='tight')
    plt.close()

def weekly_sales_trend(df_sales):
    """Plot total weekly sales trend"""
    weekly_sales = df_sales.groupby('Week_End_Date')['Qty_Sold'].sum().reset_index()
    
    plt.figure(figsize=(15, 8))
    plt.plot(weekly_sales['Week_End_Date'], weekly_sales['Qty_Sold'], marker='o', linewidth=2)
    plt.title('Total Weekly Sales Trend', fontsize=16, fontweight='bold')
    plt.xlabel('Week End Date')
    plt.ylabel('Total Quantity Sold')
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.savefig(REPORTS_CHARTS / 'weekly_sales_trend.png', dpi=300, bbox_inches='tight')
    plt.close()

def product_total_sales(df_sales):
    """Plot product-wise total sales"""
    product_sales = df_sales.groupby('Product_ID')['Qty_Sold'].sum().sort_values(ascending=False).head(20)
    
    plt.figure(figsize=(12, 8))
    ax = product_sales.plot(kind='bar')
    plt.title('Top 20 Products by Total Sales', fontsize=14, fontweight='bold')
    plt.xlabel('Product ID')
    plt.ylabel('Total Quantity Sold')
    plt.xticks(rotation=45)
    
    # Add value labels
    for p in ax.patches:
        ax.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width()/2, p.get_height() + 50), 
                   ha='center', va='bottom', fontsize=8)
    
    plt.tight_layout()
    plt.savefig(REPORTS_CHARTS / 'product_total_sales.png', dpi=300, bbox_inches='tight')
    plt.close()

def top_products(df_sales):
    """Get top 10 products by Qty_Sold"""
    top_10 = df_sales.groupby('Product_ID')['Qty_Sold'].sum().sort_values(ascending=False).head(10)
    top_10.to_csv(REPORTS_TABLES / 'top_10_products.csv')
    return top_10

def sales_distribution(df_sales):
    """Plot sales distribution histogram"""
    plt.figure(figsize=(10, 6))
    sns.histplot(data=df_sales, x='Qty_Sold', bins=50, kde=True)
    plt.title('Weekly Sales Distribution', fontsize=14, fontweight='bold')
    plt.xlabel('Quantity Sold')
    plt.ylabel('Frequency')
    plt.axvline(df_sales['Qty_Sold'].mean(), color='red', linestyle='--', label=f'Mean: {df_sales["Qty_Sold"].mean():.1f}')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig(REPORTS_CHARTS / 'sales_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()

def returns_distribution(df_sales):
    """Plot returns distribution"""
    plt.figure(figsize=(10, 6))
    sns.histplot(data=df_sales, x='Returns', bins=30, kde=True)
    plt.title('Returns Distribution', fontsize=14, fontweight='bold')
    plt.xlabel('Returns')
    plt.ylabel('Frequency')
    
    plt.tight_layout()
    plt.savefig(REPORTS_CHARTS / 'returns_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()

def discount_distribution(df_sales):
    """Plot discount distribution"""
    plt.figure(figsize=(10, 6))
    sns.histplot(data=df_sales, x='Discount', bins=30, kde=True)
    plt.title('Discount Distribution', fontsize=14, fontweight='bold')
    plt.xlabel('Discount')
    plt.ylabel('Frequency')
    
    plt.tight_layout()
    plt.savefig(REPORTS_CHARTS / 'discount_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()

def rolling_trend(df_sales):
    """Plot rolling weekly sales trend (4-week moving average)"""
    weekly_sales = df_sales.groupby('Week_End_Date')['Qty_Sold'].sum().reset_index()
    weekly_sales['Rolling_Avg'] = weekly_sales['Qty_Sold'].rolling(window=4).mean()
    
    plt.figure(figsize=(15, 8))
    plt.plot(weekly_sales['Week_End_Date'], weekly_sales['Qty_Sold'], alpha=0.5, label='Weekly Sales')
    plt.plot(weekly_sales['Week_End_Date'], weekly_sales['Rolling_Avg'], linewidth=3, color='red', label='4-Week Moving Average')
    plt.title('Rolling Weekly Sales Trend', fontsize=16, fontweight='bold')
    plt.xlabel('Week End Date')
    plt.ylabel('Total Quantity Sold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.savefig(REPORTS_CHARTS / 'rolling_sales_trend.png', dpi=300, bbox_inches='tight')
    plt.close()

def monthly_sales(df_sales):
    """Plot monthly aggregated sales"""
    df_sales_copy = df_sales.copy()
    df_sales_copy['Month'] = df_sales_copy['Week_End_Date'].dt.to_period('M')
    monthly_sales = df_sales_copy.groupby('Month')['Qty_Sold'].sum().reset_index()
    monthly_sales['Month'] = monthly_sales['Month'].astype(str)
    
    plt.figure(figsize=(15, 8))
    ax = sns.barplot(data=monthly_sales, x='Month', y='Qty_Sold')
    plt.title('Monthly Aggregated Sales', fontsize=16, fontweight='bold')
    plt.xlabel('Month')
    plt.ylabel('Total Quantity Sold')
    plt.xticks(rotation=45)
    
    # Add value labels
    for p in ax.patches:
        ax.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width()/2, p.get_height() + 1000), 
                   ha='center', va='bottom', fontsize=8)
    
    plt.tight_layout()
    plt.savefig(REPORTS_CHARTS / 'monthly_sales.png', dpi=300, bbox_inches='tight')
    plt.close()

def seasonality_visuals(df_sales):
    """Basic seasonality visuals - sales by month and day of week"""
    df_sales_copy = df_sales.copy()
    df_sales_copy['Month'] = df_sales_copy['Week_End_Date'].dt.month
    df_sales_copy['DayOfWeek'] = df_sales_copy['Week_End_Date'].dt.day_name()
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Sales by month
    monthly_avg = df_sales_copy.groupby('Month')['Qty_Sold'].mean().reset_index()
    sns.barplot(data=monthly_avg, x='Month', y='Qty_Sold', ax=ax1)
    ax1.set_title('Average Sales by Month', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Month')
    ax1.set_ylabel('Average Quantity Sold')
    
    # Sales by day of week
    dow_avg = df_sales_copy.groupby('DayOfWeek')['Qty_Sold'].mean().reset_index()
    dow_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    dow_avg['DayOfWeek'] = pd.Categorical(dow_avg['DayOfWeek'], categories=dow_order, ordered=True)
    dow_avg = dow_avg.sort_values('DayOfWeek')
    sns.barplot(data=dow_avg, x='DayOfWeek', y='Qty_Sold', ax=ax2)
    ax2.set_title('Average Sales by Day of Week', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Day of Week')
    ax2.set_ylabel('Average Quantity Sold')
    ax2.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig(REPORTS_CHARTS / 'seasonality_visuals.png', dpi=300, bbox_inches='tight')
    plt.close()

def rainfall_trend(df_external):
    """Plot rainfall trend"""
    plt.figure(figsize=(15, 6))
    plt.plot(df_external['Week_End_Date'], df_external['Rainfall'], marker='o', linewidth=2)
    plt.title('Rainfall Trend', fontsize=14, fontweight='bold')
    plt.xlabel('Week End Date')
    plt.ylabel('Rainfall (mm)')
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.savefig(REPORTS_CHARTS / 'rainfall_trend.png', dpi=300, bbox_inches='tight')
    plt.close()

def temperature_trend(df_external):
    """Plot temperature trend"""
    plt.figure(figsize=(15, 6))
    plt.plot(df_external['Week_End_Date'], df_external['Avg_Temperature'], marker='o', linewidth=2, color='orange')
    plt.title('Average Temperature Trend', fontsize=14, fontweight='bold')
    plt.xlabel('Week End Date')
    plt.ylabel('Average Temperature (°C)')
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.savefig(REPORTS_CHARTS / 'temperature_trend.png', dpi=300, bbox_inches='tight')
    plt.close()

def promo_holiday_frequency(df_external):
    """Plot promo event and holiday frequency"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10))
    
    # Promo events over time
    ax1.plot(df_external['Week_End_Date'], df_external['Promo_Event'], marker='o')
    ax1.set_title('Promo Event Frequency Over Time', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Week End Date')
    ax1.set_ylabel('Promo Event (0/1)')
    ax1.grid(True, alpha=0.3)
    ax1.set_yticks([0, 1])
    
    # Holidays over time
    ax2.plot(df_external['Week_End_Date'], df_external['Holiday'], marker='s', color='red')
    ax2.set_title('Holiday Frequency Over Time', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Week End Date')
    ax2.set_ylabel('Holiday (0/1)')
    ax2.grid(True, alpha=0.3)
    ax2.set_yticks([0, 1])
    
    plt.tight_layout()
    plt.savefig(REPORTS_CHARTS / 'promo_holiday_frequency.png', dpi=300, bbox_inches='tight')
    plt.close()

def discount_vs_sales(df_sales):
    """Plot discount vs quantity sold"""
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df_sales, x='Discount', y='Qty_Sold', alpha=0.6)
    plt.title('Discount vs Quantity Sold', fontsize=14, fontweight='bold')
    plt.xlabel('Discount')
    plt.ylabel('Quantity Sold')
    
    plt.tight_layout()
    plt.savefig(REPORTS_CHARTS / 'discount_vs_sales.png', dpi=300, bbox_inches='tight')
    plt.close()

def returns_vs_sales(df_sales):
    """Plot returns vs quantity sold"""
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df_sales, x='Returns', y='Qty_Sold', alpha=0.6)
    plt.title('Returns vs Quantity Sold', fontsize=14, fontweight='bold')
    plt.xlabel('Returns')
    plt.ylabel('Quantity Sold')
    
    plt.tight_layout()
    plt.savefig(REPORTS_CHARTS / 'returns_vs_sales.png', dpi=300, bbox_inches='tight')
    plt.close()

def weather_vs_sales(df_sales, df_external):
    """Exploratory plots of weather vs total sales"""
    # Merge sales with external features
    weekly_sales = df_sales.groupby('Week_End_Date')['Qty_Sold'].sum().reset_index()
    merged = pd.merge(weekly_sales, df_external, on='Week_End_Date', how='left')
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    
    # Rainfall vs Sales
    sns.scatterplot(data=merged, x='Rainfall', y='Qty_Sold', ax=ax1)
    ax1.set_title('Rainfall vs Total Sales', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Rainfall (mm)')
    ax1.set_ylabel('Total Quantity Sold')
    
    # Temperature vs Sales
    sns.scatterplot(data=merged, x='Avg_Temperature', y='Qty_Sold', ax=ax2)
    ax2.set_title('Temperature vs Total Sales', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Average Temperature (°C)')
    ax2.set_ylabel('Total Quantity Sold')
    
    # Sales during promo events
    promo_sales = merged.groupby('Promo_Event')['Qty_Sold'].mean().reset_index()
    sns.barplot(data=promo_sales, x='Promo_Event', y='Qty_Sold', ax=ax3)
    ax3.set_title('Average Sales: Promo vs Non-Promo Weeks', fontsize=12, fontweight='bold')
    ax3.set_xlabel('Promo Event')
    ax3.set_ylabel('Average Quantity Sold')
    ax3.set_xticks([0, 1])
    
    # Sales during holidays
    holiday_sales = merged.groupby('Holiday')['Qty_Sold'].mean().reset_index()
    sns.barplot(data=holiday_sales, x='Holiday', y='Qty_Sold', ax=ax4)
    ax4.set_title('Average Sales: Holiday vs Non-Holiday Weeks', fontsize=12, fontweight='bold')
    ax4.set_xlabel('Holiday')
    ax4.set_ylabel('Average Quantity Sold')
    ax4.set_xticks([0, 1])
    
    plt.tight_layout()
    plt.savefig(REPORTS_CHARTS / 'weather_vs_sales.png', dpi=300, bbox_inches='tight')
    plt.close()
