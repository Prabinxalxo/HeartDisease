import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pickle

def train_model():
    """
    Train a heart disease prediction model and save it as a pickle file.
    The model is based on a simplified dataset focused on the required input features.
    """
    # Create a simplified synthetic dataset for training
    # Note: In a real application, you would use actual medical data
    np.random.seed(42)
    
    # Generate 500 samples
    n_samples = 500
    
    # Generate random features
    age = np.random.randint(25, 80, n_samples)
    sex = np.random.randint(0, 2, n_samples)  # 0: female, 1: male
    cp = np.random.randint(0, 4, n_samples)   # Chest pain type
    trestbps = np.random.randint(90, 200, n_samples)  # Blood pressure
    chol = np.random.randint(120, 400, n_samples)     # Cholesterol
    
    # Create a DataFrame
    df = pd.DataFrame({
        'age': age,
        'sex': sex,
        'cp': cp,
        'trestbps': trestbps,
        'chol': chol
    })
    
    # Generate target variable with medical logic
    # Higher risk factors: older age, male, higher pain level, higher BP, higher cholesterol
    risk_score = (
        (df['age'] - 30) / 50 +  # Age factor (normalized)
        df['sex'] * 0.5 +         # Sex factor (males at higher risk)
        df['cp'] * 0.3 +          # Chest pain factor
        (df['trestbps'] - 110) / 80 +  # BP factor (normalized)
        (df['chol'] - 150) / 250       # Cholesterol factor (normalized)
    ) 
    
    # Convert risk score to binary outcome with some randomness
    threshold = risk_score.mean()
    y = (risk_score > threshold).astype(int)
    
    # Add some random variance to make the model more realistic
    random_factor = np.random.random(n_samples) * 0.3
    idx_to_flip = random_factor > 0.8
    y[idx_to_flip] = 1 - y[idx_to_flip]
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(df, y, test_size=0.2, random_state=42)
    
    # Scale the features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Create and train the model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Save the model
    with open('heart_disease_model.pkl', 'wb') as file:
        pickle.dump(model, file)
    
    # Print model accuracy on test set
    accuracy = model.score(X_test, y_test)
    print(f"Model accuracy: {accuracy:.2f}")
    
    return model

if __name__ == "__main__":
    train_model()
