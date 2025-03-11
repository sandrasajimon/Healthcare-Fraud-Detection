# Healthcare-Fraud-Detection
a group of ai aspirants trying to look for fraudulent activities in a given prescription test data

This project aims to build a robust machine learning model to detect fraudulent activities in healthcare claims using prescription data. The system leverages anomaly detection techniques such as Isolation Forest and advanced classification models to improve fraud identification accuracy.


# Project Overview
Healthcare fraud is a significant challenge that results in billions of dollars in losses each year. This project focuses on detecting suspicious claim patterns by analyzing prescription data and identifying fraudulent behavior among healthcare providers.

# Dataset Description
The dataset contains prescription data with key attributes such as:

Prescriber Information: Prscrbr_NPI, Prscrbr_Last_Org_Name, Prscrbr_First_Name, Prscrbr_City, Prscrbr_State_Abrvtn, Prscrbr_State_FIPS
Medication Details: Brnd_Name, Gnrc_Name
Claim Information: Tot_Clms, Tot_30day_Fills, Tot_Day_Suply, Tot_Drug_Cst
Patient Details: Tot_Benes, GE65_Tot_Clms, GE65_Tot_30day_Fills, etc.

These features provide insights into prescribing patterns, medication usage, and claim costs — crucial for detecting anomalies.

# Workflow

1. Data Cleaning & Preprocessing:

Handled missing values, outliers, and ensured data consistency.
Encoded categorical variables and normalized numeric values.

2. Feature Engineering:

Extracted meaningful insights such as average claim cost, total prescriptions per provider, etc.
Used correlation analysis to select key features.

3. Anomaly Detection with Isolation Forest:

Applied Isolation Forest to flag suspicious patterns in prescription data.
Evaluated precision-recall to assess model performance.

4. Classification Model Optimization:

Implemented a refined classification model with hyperparameter tuning.
Achieved 88% precision and 93% recall for fraud detection.

5. Model Evaluation:

Used a confusion matrix to visualize results, highlighting minimal false positives and effective fraud detection.

6. API Integration (Upcoming):

Designed a simple Flask API for real-time fraud detection based on model predictions.

