import pickle
import os
import sys

try:
    from sklearn.ensemble import RandomForestClassifier
    import numpy as np

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_PATH = os.path.join(BASE_DIR, 'models', 'data.pickle')
    MODEL_PATH = os.path.join(BASE_DIR, 'api', 'models', 'model.p')

    # Load the raw training data
    print(f"Loading data from {DATA_PATH}...")
    with open(DATA_PATH, 'rb') as f:
        data_dict = pickle.load(f)

    data = np.asarray(data_dict['data'])
    labels = np.asarray(data_dict['labels'])
    print(f"Data shape: {data.shape}, Labels shape: {labels.shape}")

    # Initialize a new model
    model = RandomForestClassifier(n_estimators=100, random_state=42)

    # Train the model
    print("Training model with current sklearn version...")
    model.fit(data, labels)
    
    # Verify training
    print("Training complete. Testing with a sample...")
    sample_pred = model.predict([data[0]])
    print(f"Sample prediction: {sample_pred}")

    # Save the new model to the api/models directory
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump({'model': model}, f)

    print(f"Successfully saved new model to {MODEL_PATH}")

except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
