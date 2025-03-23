# -*- coding: utf-8 -*-
"""autisense.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1KrEtjvhgf56XE30h5FZJIilMOBofNN7n

# Model Training and Optimizing
"""

# Install required packages
!pip install pandas numpy scikit-learn matplotlib seaborn

# Import necessary libraries
from google.colab import files
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, ConfusionMatrixDisplay
from sklearn.metrics import roc_auc_score, precision_recall_curve
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier

# Set random seed for reproducibility
np.random.seed(42)

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler

def load_and_preprocess_data():
    """
    Load and preprocess the dataset correctly.
    """
    print("Please upload your dataset file:")
    uploaded = files.upload()

    # Get the uploaded file name
    file_name = list(uploaded.keys())[0]

    # Load the dataset
    df = pd.read_csv(file_name)
    print("Dataset loaded successfully!")

    # Fix column names (strip spaces)
    df.columns = df.columns.str.strip()

    # Define column types
    numeric_cols = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'Age_Mons']
    categorical_cols = ['Sex', 'Ethnicity', 'Jaundice', 'Family_mem_with_ASD', 'Who completed the test']

    # Fill missing values
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())  # Fill numeric NaNs with mean
    df[categorical_cols] = df[categorical_cols].apply(lambda x: x.fillna(x.mode()[0]))  # Fill categorical NaNs with mode

    # Fix inconsistencies in categorical values
    df['Who completed the test'] = df['Who completed the test'].str.strip().str.lower()  # Convert to lowercase & remove spaces

    # Encode categorical features
    label_encoders = {}
    for col in categorical_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))  # Ensure consistent formatting
        label_encoders[col] = le

    # Prepare features and target
    features_to_drop = ['Case_No', 'Qchat-10-Score']  # Drop unnecessary columns
    X = df.drop(columns=features_to_drop + ['Class/ASD Traits'])
    y = df['Class/ASD Traits'].map({'Yes': 1, 'No': 0})  # Convert target to binary

    # Scale numeric features
    scaler = StandardScaler()
    X[numeric_cols] = scaler.fit_transform(X[numeric_cols])

    return X, y, label_encoders, scaler, numeric_cols, categorical_cols

def plot_feature_importance(model, feature_names):
    """
    Plot feature importance for tree-based models
    """
    if hasattr(model, 'feature_importances_'):
        importances = model.feature_importances_
        sorted_idx = np.argsort(importances)
        plt.figure(figsize=(10, 6))
        plt.barh(range(len(sorted_idx)), importances[sorted_idx])
        plt.yticks(range(len(sorted_idx)), np.array(feature_names)[sorted_idx])
        plt.xlabel('Feature Importance')
        plt.title('Feature Importance in Model')
        plt.tight_layout()
        plt.show()

def evaluate_model(model, X_test, y_test, model_name="Model"):
    """
    Comprehensive model evaluation
    """
    # Make predictions
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]

    # Print metrics
    print(f"\n{model_name} Evaluation:")
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    print("ROC-AUC Score:", roc_auc_score(y_test, y_pred_proba))

    # Calculate and print precision-recall metrics
    # Convert y_test to binary format (0/1) for precision_recall_curve
    y_test_binary = np.where(y_test == 'Yes', 1, 0)  # Assuming 'Yes' is the positive class
    precision, recall, _ = precision_recall_curve(y_test_binary, y_pred_proba)
    print("Average Precision:", np.mean(precision))

    # Plot confusion matrix
    plt.figure(figsize=(8, 6))
    cm = confusion_matrix(y_test, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm)
    disp.plot(cmap="Blues")
    plt.title(f"{model_name} Confusion Matrix")
    plt.show()

def train_and_compare_models(X_train, X_test, y_train, y_test):
    """
    Train and compare multiple models
    """
    models = {
        "Logistic Regression": LogisticRegression(random_state=42),
        "SVM": SVC(random_state=42, probability=True),
        "Random Forest": RandomForestClassifier(random_state=42),
        "K-Nearest Neighbors": KNeighborsClassifier(),
        "Gradient Boosting": GradientBoostingClassifier(random_state=42),
        "AdaBoost": AdaBoostClassifier(
            estimator=DecisionTreeClassifier(max_depth=1),
            n_estimators=50,
            learning_rate=1.0,
            random_state=42
        )
    }

    results = {}
    for model_name, model in models.items():
        print(f"\nTraining {model_name}...")

        # Train model
        model.fit(X_train, y_train)

        # Calculate accuracy
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        results[model_name] = accuracy

        # Calculate cross-validation scores
        cv_scores = cross_val_score(model, X_train, y_train, cv=5)
        print(f"Cross-validation scores: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")

        # Evaluate model
        evaluate_model(model, X_test, y_test, model_name)

    return models, results

def plot_model_comparison(results):
    """
    Plot comparison of model performances
    """
    plt.figure(figsize=(12, 6))
    model_names = list(results.keys())
    accuracies = list(results.values())

    plt.bar(model_names, accuracies, color='skyblue', edgecolor='black')
    plt.title('Model Comparison: Accuracy Scores', fontsize=16)
    plt.xlabel('Models', fontsize=14)
    plt.ylabel('Accuracy', fontsize=14)
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def optimize_adaboost(X_train, y_train):
    """
    Perform hyperparameter tuning for AdaBoost
    """
    param_grid = {
        'n_estimators': [50, 100, 200],
        'learning_rate': [0.01, 0.1, 1.0],
        'estimator__max_depth': [1, 2, 3]  # Changed from 'base_estimator__max_depth'
    }

    base_model = AdaBoostClassifier(estimator=DecisionTreeClassifier())
    grid_search = GridSearchCV(base_model, param_grid, cv=5, scoring='accuracy')
    grid_search.fit(X_train, y_train)

    print("\nBest parameters:", grid_search.best_params_)
    print("Best cross-validation score:", grid_search.best_score_)

    return grid_search.best_estimator_

def predict_new_data(model, new_data, label_encoders, scaler, numeric_cols, categorical_cols):
    """
    Make predictions on new data
    """
    # Preprocess new data
    for col in categorical_cols:
        if col in new_data.columns:
            new_data[col] = label_encoders[col].transform(new_data[col])

    # Scale numeric features
    new_data[numeric_cols] = scaler.transform(new_data[numeric_cols])

    # Make prediction
    prediction = model.predict(new_data)
    probability = model.predict_proba(new_data)

    return prediction, probability

# Main execution
print("Loading and preprocessing data...")
X, y, label_encoders, scaler, numeric_cols, categorical_cols = load_and_preprocess_data()

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Train and compare models
print("\nTraining and comparing models...")
models, results = train_and_compare_models(X_train, X_test, y_train, y_test)

# Plot model comparison
plot_model_comparison(results)

# Optimize AdaBoost
print("\nOptimizing AdaBoost model...")
best_adaboost = optimize_adaboost(X_train, y_train)

# Plot feature importance for the best model
print("\nPlotting feature importance...")
plot_feature_importance(best_adaboost, X.columns)

# Example of how to use the model with new data
print("\nExample of prediction with new data:")
print("To predict for new cases, create a DataFrame with the same structure as the training data")
print("(excluding 'Class/ASD Traits' and 'Qchat-10-Score'), then use the predict_new_data function")

"""# Saving and Testing the Model

"""

# Save the model and preprocessing components
import joblib

joblib.dump(best_adaboost, 'autisense_model.pkl')
joblib.dump(scaler, 'scaler.pkl')
joblib.dump(label_encoders, 'label_encoders.pkl')

print("Model and preprocessing components saved!")

import joblib
import pandas as pd

# Load trained model and preprocessing objects
model = joblib.load("autisense_model.pkl")
scaler = joblib.load("scaler.pkl")
label_encoders = joblib.load("label_encoders.pkl")

# Define a sample input (expected to have autistic traits)
sample_input = {
    "A1": 1, "A2": 1, "A3": 1, "A4": 1, "A5": 1, "A6": 1, "A7": 1, "A8": 1, "A9": 1, "A10": 1,
    "Age_Mons": 36,
    "Sex": "m",
    "Ethnicity": "White European",
    "Jaundice": "yes",
    "Family_mem_with_ASD": "yes",
    "Who completed the test": "family member"  # Changed from "parent"
}


# Convert sample input into a DataFrame
df_sample = pd.DataFrame([sample_input])

# Encode categorical features correctly
for col in label_encoders.keys():
    df_sample[col] = label_encoders[col].transform(df_sample[col])

# Scale numeric features
df_sample[numeric_cols] = scaler.transform(df_sample[numeric_cols])

# Make prediction
prediction = model.predict(df_sample)[0]
print(f"\n🔹 Prediction: {'Autistic Traits Detected' if prediction == 1 else 'No Autistic Traits Detected'}")

for feature in label_encoders.keys():
    print(f"{feature}: {list(label_encoders[feature].classes_)}")

import joblib
import pandas as pd

# Load trained model and preprocessing objects
model = joblib.load("autisense_model.pkl")
scaler = joblib.load("scaler.pkl")
label_encoders = joblib.load("label_encoders.pkl")

# Convert test cases into DataFrames
df_sample_1 = pd.DataFrame([sample_1])
df_sample_2 = pd.DataFrame([sample_2])

# Encode categorical features
for col in label_encoders.keys():
    df_sample_1[col] = label_encoders[col].transform(df_sample_1[col])
    df_sample_2[col] = label_encoders[col].transform(df_sample_2[col])

# Scale numeric features
df_sample_1[numeric_cols] = scaler.transform(df_sample_1[numeric_cols])
df_sample_2[numeric_cols] = scaler.transform(df_sample_2[numeric_cols])

# Make predictions
prediction_1 = model.predict(df_sample_1)[0]
prediction_2 = model.predict(df_sample_2)[0]

print(f"🔹 Sample 1 Prediction: {'Autistic Traits Detected' if prediction_1 == 1 else 'No Autistic Traits Detected'}")
print(f"🔹 Sample 2 Prediction: {'Autistic Traits Detected' if prediction_2 == 1 else 'No Autistic Traits Detected'}")



"""# Gradio FrontEnd"""

!pip install gradio
import gradio as gr
import joblib
import pandas as pd

# Load trained model and preprocessing objects
model = joblib.load("autisense_model.pkl")
scaler = joblib.load("scaler.pkl")
label_encoders = joblib.load("label_encoders.pkl")

# Define feature names
numeric_features = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'Age_Mons']
categorical_features = ['Sex', 'Ethnicity', 'Jaundice', 'Family_mem_with_ASD', 'Who completed the test']

def predict_autism(A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, Age_Mons, Sex, Ethnicity, Jaundice, Family_mem_with_ASD, Who_completed_test):
    """
    Preprocesses user input and predicts autism traits using the trained model.
    """
    # Create a DataFrame from user input
    input_data = pd.DataFrame([[
        A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, Age_Mons, Sex, Ethnicity, Jaundice, Family_mem_with_ASD, Who_completed_test
    ]], columns=numeric_features + categorical_features)

    # Mapping categorical inputs to match trained model
    category_mappings = {
        "Sex": {"Male": "m", "Female": "f"},
        "Jaundice": {"Yes": "yes", "No": "no"},
        "Family_mem_with_ASD": {"Yes": "yes", "No": "no"},
        "Who completed the test": {
            "Family Member": "family member",
            "Health Care Professional": "health care professional",
            "Others": "others",
            "Self": "self"
        }
    }

    # Apply mappings safely
    for col, mapping in category_mappings.items():
        input_data[col] = input_data[col].apply(lambda x: mapping.get(x, x))  # Prevents array errors

    # Encode categorical features
    for col in categorical_features:
        if col in label_encoders:  # Ensure label encoders exist for this column
            input_data[col] = label_encoders[col].transform(input_data[col])

    # Scale numeric features
    input_data[numeric_features] = scaler.transform(input_data[numeric_features])

    # Predict autism traits
    prediction = model.predict(input_data)[0]
    probabilities = model.predict_proba(input_data)[0]

    result = f"Prediction: {'Autistic Traits Detected' if prediction == 1 else 'No Autistic Traits Detected'}\n"
    result += f"Probability of No Autistic Traits: {probabilities[0]:.2%}\n"
    result += f"Probability of Autistic Traits: {probabilities[1]:.2%}"
    return result

# Define Gradio Inputs
def create_inputs():
    inputs = []

    # Numeric feature inputs
    inputs.extend([gr.Number(label=f"{feature}", minimum=0, maximum=1) for feature in numeric_features[:-1]])
    inputs.append(gr.Number(label="Age (Months)", minimum=0, maximum=240))  # Age_Mons

    # Ensure categorical values are lists (not NumPy arrays)
    ethnicity_choices = list(label_encoders["Ethnicity"].classes_)  # Convert to list
    who_completed_choices = list(label_encoders["Who completed the test"].classes_)  # Convert to list

    # Categorical feature dropdowns
    inputs.extend([
        gr.Dropdown(["Male", "Female"], label="Sex"),
        gr.Dropdown(ethnicity_choices, label="Ethnicity"),  # Fixed issue here
        gr.Dropdown(["Yes", "No"], label="Jaundice"),
        gr.Dropdown(["Yes", "No"], label="Family History of ASD"),
        gr.Dropdown(who_completed_choices, label="Who Completed the Test")  # Fixed issue here
    ])

    return inputs


# Gradio Interface
interface = gr.Interface(
    fn=predict_autism,
    inputs=create_inputs(),
    outputs=gr.Textbox(label="Prediction Results"),
    title="🧠 AutiSense: Autism Traits Detection",
    description="A machine learning tool to help detect potential autism traits."
)

# Run Gradio App
if __name__ == "__main__":
    interface.launch()

"""# Pre-Deployment Processes"""

import joblib

# Save the trained model
joblib.dump(model, "autisense_model.pkl")

# Save the scaler used for feature scaling
joblib.dump(scaler, "scaler.pkl")

# Save the label encoders for categorical data
joblib.dump(label_encoders, "label_encoders.pkl")

print("✅ Model and preprocessing objects saved successfully!")

from google.colab import files

# Download the files
files.download("autisense_model.pkl")
files.download("scaler.pkl")
files.download("label_encoders.pkl")