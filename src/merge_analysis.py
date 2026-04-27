import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Set style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Paths
REPORTS_CHARTS = Path('../reports/charts')
REPORTS_TABLES = Path('../reports/tables')

def sales_by_category(df):
    """Analyze sales by Category"""
    category_sales = df.groupby('Category')['Qty_Sold'].sum().sort_values(ascending=False).reset_index()

    plt.figure(figsize=(10, 6))
    ax = sns.barplot(data=category_sales, x='Category', y='Qty_Sold')
    plt.title('Total Sales by Category', fontsize=14, fontweight='bold')
    plt.xlabel('Category')
    plt.ylabel('Total Quantity Sold')
    plt.xticks(rotation=45)

    # Add value labels
    for p in ax.patches:
        ax.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width()/2, p.get_height() + 500),
                   ha='center', va='bottom', fontsize=10)

    plt.tight_layout()
    plt.savefig(REPORTS_CHARTS / 'sales_by_category.png', dpi=300, bbox_inches='tight')
    plt.close()

    # Save table
    category_sales.to_csv(REPORTS_TABLES / 'sales_by_category.csv', index=False)
    return category_sales

def sales_by_subcategory(df):
    """Analyze sales by Sub_Category"""
    subcategory_sales = df.groupby('Sub_Category')['Qty_Sold'].sum().sort_values(ascending=False).reset_index()

    plt.figure(figsize=(12, 6))
    ax = sns.barplot(data=subcategory_sales, x='Sub_Category', y='Qty_Sold')
    plt.title('Total Sales by Sub-Category', fontsize=14, fontweight='bold')
    plt.xlabel('Sub-Category')
    plt.ylabel('Total Quantity Sold')
    plt.xticks(rotation=45)

    # Add value labels
    for p in ax.patches:
        ax.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width()/2, p.get_height() + 300),
                   ha='center', va='bottom', fontsize=9)

    plt.tight_layout()
    plt.savefig(REPORTS_CHARTS / 'sales_by_subcategory.png', dpi=300, bbox_inches='tight')
    plt.close()

    # Save table
    subcategory_sales.to_csv(REPORTS_TABLES / 'sales_by_subcategory.csv', index=False)
    return subcategory_sales

def sales_by_gender(df):
    """Analyze sales by Gender"""
    gender_sales = df.groupby('Gender')['Qty_Sold'].sum().sort_values(ascending=False).reset_index()

    plt.figure(figsize=(8, 6))
    ax = sns.barplot(data=gender_sales, x='Gender', y='Qty_Sold')
    plt.title('Total Sales by Gender', fontsize=14, fontweight='bold')
    plt.xlabel('Gender')
    plt.ylabel('Total Quantity Sold')

    # Add value labels
    for p in ax.patches:
        ax.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width()/2, p.get_height() + 500),
                   ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig(REPORTS_CHARTS / 'sales_by_gender.png', dpi=300, bbox_inches='tight')
    plt.close()

    # Save table
    gender_sales.to_csv(REPORTS_TABLES / 'sales_by_gender.csv', index=False)
    return gender_sales

def weekly_sales_trend_by_category(df):
    """Weekly sales trend by Category"""
    category_trend = df.groupby(['Week_End_Date', 'Category'])['Qty_Sold'].sum().reset_index()

    plt.figure(figsize=(15, 8))
    sns.lineplot(data=category_trend, x='Week_End_Date', y='Qty_Sold', hue='Category', linewidth=2)
    plt.title('Weekly Sales Trend by Category', fontsize=16, fontweight='bold')
    plt.xlabel('Week End Date')
    plt.ylabel('Total Quantity Sold')
    plt.legend(title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(REPORTS_CHARTS / 'weekly_sales_trend_by_category.png', dpi=300, bbox_inches='tight')
    plt.close()

def top_categories_by_sales(df):
    """Top Categories by Qty_Sold"""
    top_categories = df.groupby('Category')['Qty_Sold'].sum().sort_values(ascending=False).head(10).reset_index()
    top_categories.to_csv(REPORTS_TABLES / 'top_categories_by_sales.csv', index=False)
    return top_categories

def top_subcategories_by_sales(df):
    """Top Sub_Categories by Qty_Sold"""
    top_subcategories = df.groupby('Sub_Category')['Qty_Sold'].sum().sort_values(ascending=False).head(10).reset_index()
    top_subcategories.to_csv(REPORTS_TABLES / 'top_subcategories_by_sales.csv', index=False)
    return top_subcategories

def discount_impact_by_category(df):
    """Discount impact by Category"""
    discount_analysis = df.groupby('Category').agg({
        'Qty_Sold': 'sum',
        'Discount': 'mean'
    }).reset_index()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # Sales by category
    sns.barplot(data=discount_analysis, x='Category', y='Qty_Sold', ax=ax1)
    ax1.set_title('Total Sales by Category', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Category')
    ax1.set_ylabel('Total Quantity Sold')
    ax1.tick_params(axis='x', rotation=45)

    # Average discount by category
    sns.barplot(data=discount_analysis, x='Category', y='Discount', ax=ax2)
    ax2.set_title('Average Discount by Category', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Category')
    ax2.set_ylabel('Average Discount (%)')
    ax2.tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.savefig(REPORTS_CHARTS / 'discount_impact_by_category.png', dpi=300, bbox_inches='tight')
    plt.close()

    # Save table
    discount_analysis.to_csv(REPORTS_TABLES / 'discount_impact_by_category.csv', index=False)
    return discount_analysis

def returns_by_category(df):
    """Returns by Category"""
    returns_analysis = df.groupby('Category').agg({
        'Qty_Sold': 'sum',
        'Returns': 'sum'
    }).reset_index()

    returns_analysis['Return_Rate'] = (returns_analysis['Returns'] / returns_analysis['Qty_Sold'] * 100).round(2)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # Returns by category
    sns.barplot(data=returns_analysis, x='Category', y='Returns', ax=ax1)
    ax1.set_title('Total Returns by Category', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Category')
    ax1.set_ylabel('Total Returns')
    ax1.tick_params(axis='x', rotation=45)

    # Return rate by category
    sns.barplot(data=returns_analysis, x='Category', y='Return_Rate', ax=ax2)
    ax2.set_title('Return Rate by Category (%)', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Category')
    ax2.set_ylabel('Return Rate (%)')
    ax2.tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.savefig(REPORTS_CHARTS / 'returns_by_category.png', dpi=300, bbox_inches='tight')
    plt.close()

    # Save table
    returns_analysis.to_csv(REPORTS_TABLES / 'returns_by_category.csv', index=False)
    return returns_analysis

def promo_event_impact(df):
    """Promo_Event impact on sales"""
    promo_analysis = df.groupby('Promo_Event').agg({
        'Qty_Sold': ['sum', 'mean'],
        'Discount': 'mean'
    }).round(2)

    promo_analysis.columns = ['Total_Sales', 'Avg_Weekly_Sales', 'Avg_Discount']
    promo_analysis = promo_analysis.reset_index()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # Average sales during promo vs non-promo
    sns.barplot(data=promo_analysis, x='Promo_Event', y='Avg_Weekly_Sales', ax=ax1)
    ax1.set_title('Average Weekly Sales: Promo vs Non-Promo', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Promo Event')
    ax1.set_ylabel('Average Weekly Sales')
    ax1.set_xticks([0, 1])

    # Average discount during promo vs non-promo
    sns.barplot(data=promo_analysis, x='Promo_Event', y='Avg_Discount', ax=ax2)
    ax2.set_title('Average Discount: Promo vs Non-Promo', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Promo Event')
    ax2.set_ylabel('Average Discount (%)')
    ax2.set_xticks([0, 1])

    plt.tight_layout()
    plt.savefig(REPORTS_CHARTS / 'promo_event_impact.png', dpi=300, bbox_inches='tight')
    plt.close()

    # Save table
    promo_analysis.to_csv(REPORTS_TABLES / 'promo_event_impact.csv', index=False)
    return promo_analysis

def holiday_impact(df):
    """Holiday impact on sales"""
    holiday_analysis = df.groupby('Holiday').agg({
        'Qty_Sold': ['sum', 'mean'],
        'Returns': 'mean'
    }).round(2)

    holiday_analysis.columns = ['Total_Sales', 'Avg_Weekly_Sales', 'Avg_Returns']
    holiday_analysis = holiday_analysis.reset_index()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # Average sales during holiday vs non-holiday
    sns.barplot(data=holiday_analysis, x='Holiday', y='Avg_Weekly_Sales', ax=ax1)
    ax1.set_title('Average Weekly Sales: Holiday vs Non-Holiday', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Holiday')
    ax1.set_ylabel('Average Weekly Sales')
    ax1.set_xticks([0, 1])

    # Average returns during holiday vs non-holiday
    sns.barplot(data=holiday_analysis, x='Holiday', y='Avg_Returns', ax=ax2)
    ax2.set_title('Average Returns: Holiday vs Non-Holiday', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Holiday')
    ax2.set_ylabel('Average Returns')
    ax2.set_xticks([0, 1])

    plt.tight_layout()
    plt.savefig(REPORTS_CHARTS / 'holiday_impact.png', dpi=300, bbox_inches='tight')
    plt.close()

    # Save table
    holiday_analysis.to_csv(REPORTS_TABLES / 'holiday_impact.csv', index=False)
    return holiday_analysis

def weather_vs_sales_analysis(df):
    """Weather (Rainfall / Avg_Temperature) vs Qty_Sold exploratory analysis"""
    # Aggregate weekly sales
    weekly_sales = df.groupby('Week_End_Date').agg({
        'Qty_Sold': 'sum',
        'Rainfall': 'first',
        'Avg_Temperature': 'first'
    }).reset_index()

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))

    # Rainfall vs Total Sales
    sns.scatterplot(data=weekly_sales, x='Rainfall', y='Qty_Sold', ax=ax1, alpha=0.7)
    ax1.set_title('Rainfall vs Total Weekly Sales', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Rainfall (mm)')
    ax1.set_ylabel('Total Weekly Sales')

    # Temperature vs Total Sales
    sns.scatterplot(data=weekly_sales, x='Avg_Temperature', y='Qty_Sold', ax=ax2, alpha=0.7)
    ax2.set_title('Temperature vs Total Weekly Sales', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Average Temperature (°C)')
    ax2.set_ylabel('Total Weekly Sales')

    # Rainfall distribution
    sns.histplot(data=weekly_sales, x='Rainfall', ax=ax3, kde=True)
    ax3.set_title('Rainfall Distribution', fontsize=12, fontweight='bold')
    ax3.set_xlabel('Rainfall (mm)')
    ax3.set_ylabel('Frequency')

    # Temperature distribution
    sns.histplot(data=weekly_sales, x='Avg_Temperature', ax=ax4, kde=True)
    ax4.set_title('Temperature Distribution', fontsize=12, fontweight='bold')
    ax4.set_xlabel('Average Temperature (°C)')
    ax4.set_ylabel('Frequency')

    plt.tight_layout()
    plt.savefig(REPORTS_CHARTS / 'weather_vs_sales_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()

    # Save correlation analysis
    correlation = weekly_sales[['Qty_Sold', 'Rainfall', 'Avg_Temperature']].corr()
    correlation.to_csv(REPORTS_TABLES / 'weather_sales_correlation.csv')

    return correlation