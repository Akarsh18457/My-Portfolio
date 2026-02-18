📧 Email Spam Classifier using Naive Bayes

A Machine Learning project that classifies emails as Spam or Not Spam (Ham) using Multinomial Naive Bayes with TF-IDF vectorization.

This project demonstrates practical implementation of NLP, probabilistic modeling, and deployment using Streamlit.

🚀 Project Overview

Spam detection is a classic Natural Language Processing (NLP) problem where the goal is to automatically filter unwanted or malicious emails.

This model analyzes the textual content of an email and predicts whether it is:

Spam

Ham (Legitimate Email)

The system is trained on the spam.csv dataset and deployed as an interactive web app.

🧠 Machine Learning Approach
🔹 Algorithm Used: Multinomial Naive Bayes

Naive Bayes is a probabilistic classifier based on Bayes’ Theorem, assuming conditional independence between features.

It is highly effective for:

Text classification problems

High-dimensional sparse data

Fast and scalable predictions

🔹 Feature Engineering: TF-IDF Vectorizer

Instead of simple word counts, this project uses:

TF-IDF (Term Frequency – Inverse Document Frequency)

TF-IDF helps:

Reduce the weight of common words

Increase importance of rare but meaningful words

Improve classification performance

📊 Model Performance
Metric	Score
Accuracy	97%
Precision	100%

🔍 Interpretation

97% Accuracy → Model performs extremely well overall.

100% Precision → No legitimate email was incorrectly classified as spam.

High precision is crucial in spam filtering systems because false positives (marking genuine emails as spam) can be costly.

🔄 Workflow

Data Cleaning

Text Preprocessing

Lowercasing

Tokenization

Stopword Removal

Punctuation Removal

TF-IDF Vectorization

Model Training (Multinomial Naive Bayes)

Model Evaluation

Streamlit Deployment

🔬 Model Experimentation & Comparison

To ensure the best-performing model was selected, multiple machine learning algorithms were evaluated.

🔹 Algorithms Tested (11 Models)

Logistic Regression

K-Nearest Neighbors (KNN)

Support Vector Machine (SVM)

Decision Tree

Random Forest

Gradient Boosting

AdaBoost

Extra Trees Classifier

Bernoulli Naive Bayes

Multinomial Naive Bayes

Complement Naive Bayes

🔹 Ensemble Techniques Explored

Voting Classifier

Stacking Classifier

Each model was evaluated using:

Accuracy

Precision

After comparative evaluation, Multinomial Naive Bayes (MNB) was shortlisted as the final model due to:

Highest precision performance

Strong overall accuracy

Fast training and inference time

Better suitability for sparse TF-IDF text features

Lower computational complexity compared to ensemble models

🌐 Streamlit Web App

The trained model is deployed using Streamlit, allowing users to input email text and instantly receive predictions.

Features:

Clean and simple UI

Real-time spam detection

Lightweight deployment

Fast inference

Run Locally
pip install -r requirements.txt
streamlit run app.py

🛠 Tech Stack

Python

Scikit-learn

Pandas

NumPy

NLTK

TF-IDF Vectorizer

Streamlit


📌 Key Highlights

Compared 11 machine learning algorithms

Implemented ensemble techniques (Voting & Stacking)

Selected best model based on performance metrics

Achieved 100% precision

Built end-to-end NLP classification pipeline

Deployed using Streamlit

🔮 Future Improvements

Hyperparameter tuning with GridSearchCV

Cross-validation for stronger generalization

Deploy on cloud (Render / AWS / HuggingFace Spaces)

Add explainability using SHAP

Expand dataset for better robustness
👨‍💻 Author

Akarsh Jain
Aspiring Data Scientist | Machine Learning Enthusiast

If you found this project useful, feel free to ⭐ the repository.
