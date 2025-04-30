import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

# Load and prepare the data
print("Loading test data...")
df = pd.read_csv('smart_home_data.csv')

# Prepare features
device_columns = ['watch_tv', 'play_music', 'smart_locks', 'security_cameras', 
                 'security_system', 'water_heater_status']
light_columns = ['bedroom_light', 'living_room_light', 'bathroom_light', 'kitchen_light']

# Convert categorical variables
label_encoders = {}
categorical_columns = ['mood', 'person_condition', 'time_of_day']
X_encoded = pd.DataFrame()

for column in categorical_columns:
    label_encoders[column] = LabelEncoder()
    X_encoded[column] = label_encoders[column].fit_transform(df[column])

# Add numeric columns
X_encoded['at_home'] = df['at_home']
X_encoded['is_holiday'] = df['is_holiday']

# Split data - use 20% for testing
X_train, X_test, y_devices_train, y_devices_test = train_test_split(
    X_encoded, df[device_columns], test_size=0.2, random_state=42
)
_, _, y_lights_train, y_lights_test = train_test_split(
    X_encoded, df[light_columns], test_size=0.2, random_state=42
)
_, _, y_music_train, y_music_test = train_test_split(
    X_encoded, df['music_type'], test_size=0.2, random_state=42
)

print(f"\nTesting on {len(X_test)} samples")

# Create and train models
print("\nTraining models...")
device_model = RandomForestClassifier(n_estimators=100, random_state=42)
light_model = RandomForestClassifier(n_estimators=100, random_state=42)
music_model = RandomForestClassifier(n_estimators=100, random_state=42)

device_model.fit(X_train, y_devices_train)
light_model.fit(X_train, y_lights_train)

# For music type
music_encoder = LabelEncoder()
y_music_train_encoded = music_encoder.fit_transform(y_music_train)
music_model.fit(X_train, y_music_train_encoded)

# Make predictions
print("Making predictions...")
device_predictions = device_model.predict(X_test)
light_predictions = light_model.predict(X_test)
music_predictions = music_model.predict(X_test)
music_predictions = music_encoder.inverse_transform(music_predictions)

# Calculate accuracy
print("Calculating accuracy...")
device_accuracy = {}
for i, col in enumerate(device_columns):
    accuracy = accuracy_score(y_devices_test[col], device_predictions[:, i])
    device_accuracy[col] = accuracy

light_accuracy = {}
for i, col in enumerate(light_columns):
    accuracy = accuracy_score(y_lights_test[col], light_predictions[:, i])
    light_accuracy[col] = accuracy

music_accuracy = accuracy_score(y_music_test, music_predictions)

# Print results
print("\nTest Results:")
print("-" * 50)

print("\nDevice Control Accuracy:")
for device, accuracy in device_accuracy.items():
    print(f"{device.replace('_', ' ').title()}: {accuracy:.2f}")

print("\nLight Control Accuracy:")
for light, accuracy in light_accuracy.items():
    print(f"{light.replace('_', ' ').title()}: {accuracy:.2f}")

print(f"\nMusic Type Prediction Accuracy: {music_accuracy:.2f}")

# Show example predictions
print("\nDetailed Examples (First 50 samples):")
print("-" * 50)

correct_predictions = {
    'devices': 0,
    'lights': 0,
    'music': 0
}

for i in range(50):
    print(f"\nSample {i+1}:")
    
    # Get original feature values
    sample = X_test.iloc[i]
    original_mood = label_encoders['mood'].inverse_transform([int(sample['mood'])])[0]
    original_condition = label_encoders['person_condition'].inverse_transform([int(sample['person_condition'])])[0]
    original_time = label_encoders['time_of_day'].inverse_transform([int(sample['time_of_day'])])[0]
    
    print("Input Features:")
    print(f"Mood: {original_mood}")
    print(f"Condition: {original_condition}")
    print(f"Time of Day: {original_time}")
    print(f"At Home: {int(sample['at_home'])}")
    print(f"Is Holiday: {int(sample['is_holiday'])}")
    
    # Get actual and predicted values
    actual_devices = {col: int(y_devices_test.iloc[i][col]) for col in device_columns}
    actual_lights = {col: int(y_lights_test.iloc[i][col]) for col in light_columns}
    actual_music = y_music_test.iloc[i]
    
    pred_devices = {col: int(pred) for col, pred in zip(device_columns, device_predictions[i])}
    pred_lights = {col: int(pred) for col, pred in zip(light_columns, light_predictions[i])}
    pred_music = music_predictions[i]
    
    print("\nActual values:")
    print("Devices:", actual_devices)
    print("Lights:", actual_lights)
    print("Music:", actual_music)
    
    print("\nPredicted values:")
    print("Devices:", pred_devices)
    print("Lights:", pred_lights)
    print("Music:", pred_music)
    
    # Check if predictions are correct
    if actual_devices == pred_devices:
        correct_predictions['devices'] += 1
    if actual_lights == pred_lights:
        correct_predictions['lights'] += 1
    if actual_music == pred_music:
        correct_predictions['music'] += 1

# Print accuracy for the 50 samples
print("\nAccuracy for the 50 detailed samples:")
print("-" * 50)
print(f"Devices: {(correct_predictions['devices'] / 50) * 100:.2f}%")
print(f"Lights: {(correct_predictions['lights'] / 50) * 100:.2f}%")
print(f"Music: {(correct_predictions['music'] / 50) * 100:.2f}%") 