# Autisense: Autism Prediction and Privacy-Preserving Healthcare System

## 🔍 Project Overview
**Autisense** is a machine-learning-powered platform designed to assist healthcare professionals in predicting autism in toddlers. This project provides a secure and privacy-compliant environment where doctors can input patient data, receive AI-driven predictions, and ensure data security through privacy-preserving techniques.

## 🎯 Key Features
- **Autism Prediction Model**: Uses **AdaBoost** for high-accuracy predictions.
- **Role-Based Access Control (RBAC)**:
  - **Doctors**: Can input patient data, run the model, and get predictions.
  - **Patients**: Can view their own diagnosis and reports.
  - **Researchers**: Access anonymized patient data for research purposes.
- **Privacy-Preserving Techniques:** Implements perturbation to protect sensitive data.
- **Security Measures**: Authentication, encryption, and access control mechanisms.
- **Gradio-Based Web Interface**: User-friendly UI for doctors, patients, and researchers.

## 📂 Dataset
The project utilizes the **Toddler Autism Screening Dataset** from Kaggle:
- **Dataset Name**: [Autism Screening for Toddlers](https://www.kaggle.com/datasets/fabdelja/autism-screening-for-toddlers?resource=download&select=Toddler+Autism+dataset+July+2018.csv)
- **Features**:
  - **Behavioral traits** (A1-A10 responses)
  - **Age in months**
  - **Q-CHAT Score**
  - **Demographics** (Sex, Ethnicity, Jaundice history, Family ASD history)
  - **Target Variable**: `Class/ASD Traits` (Indicating presence of ASD traits)
 
## Privacy & Security Measures
- **Perturbation:** Random noise is added to sensitive data to prevent exact identification.
- **Encryption:** User information is securely stored.
- **Access Control:** Role-based authentication restricts unauthorized access.


![Screenshot 2025-04-01 022852](https://github.com/user-attachments/assets/0864301e-5a55-4545-a89e-aa93cc5a9414)
![Screenshot 2025-04-01 022909](https://github.com/user-attachments/assets/7955e32a-1fb8-4310-a76c-b9d336883668)


## 🚀 Installation & Setup
### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/autisense.git
cd autisense
```

### 2️⃣ Install Dependencies
Ensure you have Python installed (preferably **Python 3.8+**). Install required packages:
```bash
pip install -r requirements.txt
```

### 3️⃣ Run the Application
```bash
python app.py
```

## 🏗️ Project Architecture
```
Autisense/
│-- dataset/                     # Autism screening dataset
│-- models/                      # Trained model and encoders
│   │-- autisense_model.pkl      # Trained AdaBoost model
│   │-- scaler.pkl               # Standard Scaler for preprocessing
│   │-- label_encoders.pkl       # Encoders for categorical variables
│-- neura.py                      # Core ML processing script
│-- app.py                        # Gradio-based Web UI
│-- requirements.txt              # Dependencies
│-- README.md                     # Documentation
```

## 🔑 Role-Based Access Control (RBAC)
| **Role**     | **Permissions** |
|-------------|----------------|
| **Doctor**  | Input patient data, run model, view predictions |
| **Patient** | View only their own results |
| **Researcher** | Access anonymized data for research |

## 🛡️ Privacy & Security Features
- **Perturbation**: Adds minor noise to data for anonymization.
- **k-Anonymity**: Groups data to prevent individual identification.
- **Secure Sum Protocol**: Ensures no direct data sharing between parties.
- **Encryption & Authentication**: Secure access to data and model predictions.

## 🤖 Model Training & Performance
- **Algorithm**: **AdaBoost Classifier**
- **Evaluation Metrics**:
  - Accuracy: **~90%**
  - Precision, Recall, F1-Score for balanced evaluation
- **Preprocessing**:
  - Categorical encoding for demographic features
  - Standard scaling for numerical values
  - Train-test split with stratification

## 🌍 Deployment
### 🎯 Deploy on Hugging Face Spaces
1. **Install Spaces CLI**
   ```bash
   pip install huggingface_hub
   ```
2. **Login to Hugging Face**
   ```bash
   huggingface-cli login
   ```
3. **Push to Spaces**
   ```bash
   git push origin main
   ```

## 📌 Future Enhancements
- 🏥 **Integration with Electronic Health Records (EHR)**
- 🛠️ **Implementing more advanced privacy-preserving techniques**
- 📊 **Expanding dataset & retraining models for better generalization**

## 📜 License
This project is licensed under the **MIT License**.

---

🚀 **Autisense** is a step towards AI-driven, privacy-preserving autism screening! If you found this project helpful, consider ⭐ starring the repository! 🌟

