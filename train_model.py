"""
Leaf Disease Detection ML Model Training
Uses scikit-learn to train a classifier for plant disease detection
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import joblib
import os
import sys

MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'disease_model.pkl')
ENCODER_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'label_encoder.pkl')
DATASET_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'leaf_disease_dataset.csv')

def train_model():
    print("=" * 50)
    print("Leaf Disease Detection - ML Model Training")
    print("=" * 50)
    
    try:
        df = pd.read_csv(DATASET_PATH)
        print(f"\nDataset loaded: {len(df)} samples")
        print(f"Features: {list(df.columns)}")
        
        X = df[['leaf_color_avg', 'green_ratio', 'brown_spots_ratio', 
                'yellow_spots_ratio', 'dark_spots_ratio', 'lesion_size', 'spot_count']]
        y = df['disease_type']
        
        le_disease = LabelEncoder()
        y_encoded = le_disease.fit_transform(y)
        
        print(f"\nDisease classes: {len(le_disease.classes_)} classes")
        print(f"Samples per class:\n{df['disease_type'].value_counts()}")
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_encoded, test_size=0.2, random_state=42
        )
        
        print("\nTraining Random Forest Classifier...")
        model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=2,
            min_samples_leaf=1,
            random_state=42,
            n_jobs=-1
        )
        
        model.fit(X_train, y_train)
        
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"\nModel Training Complete!")
        print(f"Accuracy: {accuracy * 100:.2f}%")
        
        feature_importance = pd.DataFrame({
            'feature': X.columns,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        print("\nFeature Importance:")
        print(feature_importance)
        
        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
        joblib.dump(model, MODEL_PATH)
        joblib.dump(le_disease, ENCODER_PATH)
        
        print(f"\nModel saved to: {MODEL_PATH}")
        print(f"Label encoder saved to: {ENCODER_PATH}")
        
        return model, le_disease, accuracy
        
    except Exception as e:
        print(f"Error during training: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

def load_model():
    try:
        model = joblib.load(MODEL_PATH)
        le = joblib.load(ENCODER_PATH)
        print("Pre-trained model loaded successfully")
        return model, le
    except FileNotFoundError:
        print("No pre-trained model found. Training new model...")
        return train_model()

def predict_disease(features):
    model, le = load_model()
    feature_names = ['leaf_color_avg', 'green_ratio', 'brown_spots_ratio', 
                     'yellow_spots_ratio', 'dark_spots_ratio', 'lesion_size', 'spot_count']
    X = pd.DataFrame([features], columns=feature_names)
    prediction = model.predict(X)
    probability = model.predict_proba(X)
    predicted_class = le.inverse_transform(prediction)[0]
    confidence = max(probability[0]) * 100
    return predicted_class, confidence

if __name__ == '__main__':
    train_model()
    
    print("\n" + "=" * 50)
    print("Testing Model with Sample Data...")
    print("=" * 50)
    
    sample_data = [45.2, 0.65, 0.12, 0.03, 0.08, 2.5, 15]
    
    result, conf = predict_disease(sample_data)
    print(f"Test Prediction: {result} (Confidence: {conf:.2f}%)")
