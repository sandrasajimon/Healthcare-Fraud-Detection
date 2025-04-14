# Healthcare-Fraud-Detection using AI
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

6. Real-Time Prediction with Streamlit UI:

Instead of using a separate Flask API, real-time fraud detection was implemented directly within the Streamlit application. The trained fraud detection model (saved as fraud_model.joblib) is loaded into the app using joblib.load(), and users can input new prescriber or transaction data through an interactive form in the Streamlit interface.

Once the user submits the form, the input is preprocessed and passed into the model in real time. The app instantly displays the prediction — such as whether the input indicates fraudulent or non-fraudulent activity — making it interactive and user-friendly.

# Conclusion
The Prescriber Analyzer project demonstrates the potential of combining machine learning with interactive data applications to detect fraudulent prescriber behavior in real time. Built entirely with Streamlit, this application enables users to:

Search and filter prescribers by state and National Provider Identifier (NPI)

Visualize geographic trends in prescribing behavior across the U.S.

Detect potential fraud using a pre-trained machine learning model integrated into the app

Download filtered data for further analysis

The project highlights how a user-friendly interface, powered by AI and real-time analytics, can assist healthcare administrators and investigators in monitoring Medicare Part D data effectively.

With a clean, responsive UI and seamless integration of backend model predictions, this solution is a scalable prototype for real-world fraud detection in healthcare systems.

"Turning data into decisions – one prediction at a time."




# References

Data is collected from https://data.cms.gov/provider-summary-by-type-of-service/medicare-part-d-prescribers/medicare-part-d-prescribers-by-provider-and-drug/data

# Contributors
Devika Dileep - Healthcare Analyst
Sandra Sajimon - Project Manager
John Hanok - Data Scientist / ML Engineer

