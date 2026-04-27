Data Understanding

2.1 Objective of This Phase

The main objective of this phase is to understand the structure, content, and usefulness of the available datasets before starting any preprocessing or modeling.

This phase helps answer questions like:

What data is available?
What does each dataset represent?
What is the target variable?
Which dataset contains time-based information?
Which columns can be used later as features?
Are the datasets suitable for weekly demand forecasting?

A proper understanding at this stage is important because forecasting quality depends heavily on the quality and relevance of the input data.

2.2 Datasets Available

The project currently uses two main datasets for the forecasting workflow:

Dataset 1: Product_Information

This dataset contains static product-level information.

Each row represents a product and its attributes.

Main purpose of this dataset:

It provides descriptive and business-related context about each product, which can later be used for:

segmentation
demand analysis
feature engineering
business interpretation
Typical information expected in this dataset:
Product_ID
Category
Sub_Category
Gender
Launch_Date
MSRP
other product-related fields

Role in the project:

This dataset does not directly contain demand over time, but it is important because it helps explain why some products may behave differently from others.

For example:

some categories may have stable demand
some sub-categories may be more seasonal
gender-based product groups may show different sales patterns

So this dataset acts as a product master / dimension table.

Dataset 2: Weekly_Sales

This is the main forecasting dataset.

It contains the historical weekly sales performance of products.

Each row represents a product’s demand and related sales activity for a specific week.

Main purpose of this dataset:

This dataset provides the time series demand behavior needed for forecasting.

Typical information expected in this dataset:
Week_End_Date
Product_ID
Qty_Sold
Returns
Discount
stock or inventory-related variables
Role in the project:

This dataset contains the target variable and is the most important source for:

trend analysis
seasonality analysis
demand classification
feature engineering
forecasting model training

This is the dataset that will be used to study how demand changes over time for each product.

2.3 Target Variable Identification

For this project, the main variable to be forecasted is:

Qty_Sold

Why this is the target:

Qty_Sold represents the number of units sold for a product in a given week.

This makes it the most suitable variable for demand forecasting because it directly reflects product demand over time.

Forecasting target:
What to predict? → Qty_Sold
At what level? → Product level
At what frequency? → Weekly

2.4 Time Granularity of the Problem

The forecasting problem is designed at the:

Weekly level

This means the time series is based on:

Week_End_Date
Why weekly granularity matters:

Weekly demand forecasting is useful because it captures:

short-term fluctuations
product demand movement
demand variability
early seasonal patterns

It is also more detailed than monthly forecasting and therefore more suitable for building accurate forecasting models.

Even though the final output may later be shown at the monthly level, the actual forecasting work is done weekly.

2.5 Unit of Analysis

The core unit of analysis in this project is:

Product × Week

This means each observation in the forecasting dataset represents:

one product in one specific week

Example:

Product_ID	Week_End_Date	Qty_Sold
TE001	    2023-01-07	        25
TE001	    2023-01-14	        30
TE002	    2023-01-07	        12

This is important because the project is not just forecasting total company sales.

It is forecasting demand at a more useful and detailed level:

product-level weekly demand

2.6 Role of Each Dataset in the Project

It is important to understand how each dataset contributes to the forecasting system.

Product_Information contributes:
product identity
category mapping
sub-category mapping
gender segmentation
product age / launch information
static descriptive features
Weekly_Sales contributes:
historical demand
weekly product behavior
sales trend
zero-demand patterns
discount / return / stock-related signals
time series forecasting target
Combined use after merge:

Once merged, these datasets help answer:

Which categories are high-demand?
Which products are intermittent?
Which product groups are more stable?
Which features help forecasting?

This merged dataset becomes the base for:

EDA
demand classification
feature engineering
modeling