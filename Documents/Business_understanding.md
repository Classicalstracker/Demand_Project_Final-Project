Business Understanding

This phase is about clearly defining:

what problem we are solving
why it matters
what exactly we are forecasting
how the output will be used


1.1 Project Objective
Main Objective

Build a product-level demand forecasting system for Trail Edge using historical weekly sales data and product information.

The goal is to forecast future product demand in a way that supports:

inventory planning
replenishment decisions
demand visibility
product performance understanding

1.2 Business Problem Statement

Trail Edge sells multiple products across different:

categories
sub-categories
genders

However, not all products behave the same way.

Some products may show:

stable and regular demand
irregular fluctuations
intermittent demand with many zero-sales weeks
highly unpredictable or lumpy demand

Because of this, applying one single forecasting approach to all products may not give reliable results.

So, the business problem is:

How can we build a weekly demand forecasting system that first understands product demand behavior and then identifies the most suitable forecasting model for each product or demand pattern?

1.3 Why This Problem Matters

Accurate demand forecasting is important because it directly impacts business operations.

A good forecasting system helps in:

Inventory Optimization
avoid overstocking slow-moving products
reduce stockouts for high-demand products
Better Planning
improve replenishment and allocation decisions
support planning across categories and sub-categories
Business Visibility
identify which products are stable vs difficult to predict
understand demand trends by category, gender, and product group
Model Efficiency
use the right model for the right demand pattern instead of forcing one model on all products

1.4 Forecasting Goal

The forecasting goal for this project is:

To predict future weekly demand (Qty_Sold) for each product

This means:

Target variable = Qty_Sold
Forecasting unit = Product_ID
Time granularity = Weekly

1.5 Forecasting Design

This is a very important section.

Because your project has two different levels:

Modeling Level

Forecasting will be performed at the:

Weekly level

Why?

Because your historical sales data is available weekly, and weekly modeling captures:

short-term demand movement
product-level fluctuations
seasonality patterns more accurately
Business Output Level

Even though forecasting is done weekly, the final business-facing output will also be shown at:

Monthly level

Why?

Because monthly output is easier for:

business reporting
planning summaries
category-level review
demand communication

So:

Project logic:
Train and forecast weekly
Aggregate output to monthly

1.6 Forecast Horizon

The forecasting horizon for this project is:

Next 3 months

This means:

weekly predictions will be generated for the future horizon
these weekly forecasts will then be rolled up into monthly summaries

1.7 Core Analytical Strategy

This is the most important intelligence layer in your project.

Instead of directly forecasting all products in the same way, this project will first:

Classify products based on demand behavior

Products will be segmented into:

Smooth
Erratic
Intermittent
Lumpy

Why?

Because different products behave differently, and forecasting should reflect that.

This helps answer:

which products are easy to forecast?
which products are difficult?
which forecasting models are more suitable for each type?

This makes the forecasting process more realistic and business-relevant.

1.8 Modeling Strategy

The project will follow a model selection and tuning approach, rather than using a one-size-fits-all model.

That means:

suitable forecasting models will be shortlisted
internal features will be created from historical sales data
hyperparameter tuning will be performed
the best model and best parameter combination will be selected

This selected setup will later be used for forecasting.

So the project focus is not just:

“Build any forecast”

Instead, it is:

“Find the most suitable forecasting setup for each product or demand segment.”

1.9 Scope of Work (Current Phase Scope)

For the current project stage, the focus is only up to:

Model evaluation and cross-validation

So the current work includes:

understanding the data
preprocessing
EDA
merging
demand classification
feature engineering
model selection
hyperparameter tuning
time series cross-validation
Not included in current scope (for now):
final future forecast generation
external feature modeling
chatbot


1.10 Expected Business Outcomes

By the end of the current project scope, the expected outcomes are:

1. Product Demand Segmentation

Each product will be classified into a demand type:

Smooth / Erratic / Intermittent / Lumpy

2. Forecasting Readiness

A clean, structured, model-ready weekly forecasting dataset will be created

3. Best Model Identification

For each product / demand segment, the most suitable model and parameters will be identified

4. Evaluation Framework

A proper time series cross-validation setup will be established to evaluate forecasting performance

1.11 Final One-Line Project Definition


This project aims to build a weekly product-level demand forecasting system for Trail Edge by first understanding demand behavior, segmenting products into demand classes, and then identifying the best tuned forecasting model using internal sales-driven features.