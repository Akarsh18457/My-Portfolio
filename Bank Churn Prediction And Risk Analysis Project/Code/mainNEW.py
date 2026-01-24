import os
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestClassifier

MODEL_FILE = "model.pkl"
PIPELINE_FILE = "pipeline.pkl"

def build_pipeline(num_attribs, cat_attribs):
    num_pipeline = Pipeline([
    ("scaler", StandardScaler())
    ])

    cat_pipeline = Pipeline([
    ("onehot", OneHotEncoder(handle_unknown="ignore"))
    ])

    full_pipeline = ColumnTransformer([
    ("num", num_pipeline, num_attribs),
    ("cat", cat_pipeline, cat_attribs)
    ])
    return full_pipeline

if not os.path.exists(MODEL_FILE):

    churn = pd.read_csv("Churn_Modelling.csv")

    churn["Age_cat"] = pd.cut(churn["Age"], bins=[15,25,35,45,55,65,75,85,95], labels=[1, 2, 3, 4, 5, 6, 7, 8])

    split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
    for train_index, test_index in split.split(churn, churn["Age_cat"]):
        churn.loc[test_index].drop("Age_cat", axis=1).to_csv("Test Data.csv", index=False)
        churn = churn.loc[train_index].drop("Age_cat", axis=1)

    churn_labels = churn["Exited"].copy()
    churn_features = churn.drop("Exited", axis=1)

    num_attribs = ["CreditScore", "Age", "Tenure", "Balance", "NumOfProducts", "HasCrCard", "IsActiveMember", "EstimatedSalary"]
    cat_attribs = ["Geography", "Gender"]

    pipeline = build_pipeline(num_attribs, cat_attribs)
    churn_prepared = pipeline.fit_transform(churn_features)

    model = RandomForestClassifier(random_state=42)
    model.fit(churn_prepared, churn_labels)

    joblib.dump(model, MODEL_FILE)
    joblib.dump(pipeline, PIPELINE_FILE)

    print("Model is trained and saved successfully!")

else:
    model = joblib.load(MODEL_FILE)
    pipeline = joblib.load(PIPELINE_FILE)

    input_data = pd.read_csv("input.csv")
    transformed_input = pipeline.transform(input_data)
    predictions = model.predict(transformed_input)
    input_data["Exited"] = predictions

    input_data.to_csv("Test Output Data.csv", index=False)
    print("Inference complete. Results are saved to output.csv")




