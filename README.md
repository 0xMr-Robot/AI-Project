# 🏡✨ Smart Home Automation AI Project

Welcome to the **Smart Home Automation AI Project**! This project leverages machine learning to create an intelligent system that predicts and recommends optimal settings for various smart home devices, lights, and music based on user context and mood. Dive in to discover how your home can become smarter, more adaptive, and truly personalized! 🌟

---

## 📂 Project Structure

```
AI-Project/
│
├── real_model.py         # Main AI model and logic
├── smart_home_data.csv   # Training data (not included here)
├── model_performance_history.csv # Model performance log
└── README.md             # This file
```

---

## 🚀 What Does This Project Do?

This project uses real-world-like data to train machine learning models that:
- **Predict the status of smart devices** (TV, locks, cameras, security system, water heater)
- **Recommend light brightness levels** for each room
- **Suggest music types** based on mood and context

All predictions are made using a combination of user mood, condition, time, and home context. The system is designed to be robust, handling unknown or unexpected input values gracefully.

---

## 🧠 How Does It Work?

### 1. **Data Loading & Preprocessing**
- Loads data from `smart_home_data.csv`.
- Extracts features from date/time (month, day of week, hour, weekend flag).
- Encodes categorical variables (mood, person condition, time of day, etc.) into numbers for ML models.
- Handles unknown or new input values with smart mapping and fallback logic.

### 2. **Feature Engineering**
- **Input Features:**
  - `mood` (e.g., happy, tired, stressed)
  - `person_condition` (e.g., at_home, sleeping, at_work)
  - `time_of_day` (morning, afternoon, evening, night)
  - `at_home` (1 if home, 0 if away)
  - `is_holiday` (1 if holiday, 0 otherwise)
- **Output Features:**
  - **Devices:** TV, smart locks, security cameras, security system, water heater
  - **Lights:** Bedroom, living room, bathroom, kitchen (brightness 0-100%)
  - **Music:** Music type (categorical)

### 3. **Model Training**
- **Device Control:** Random Forest Classifier
- **Light Control:** Multi-Layer Perceptron (MLP) Regressor
- **Music Recommendation:** Random Forest Classifier (with label encoding)

### 4. **Prediction Logic**
- Accepts user context (mood, condition, time, etc.)
- Handles unknown values with smart mapping or fallback
- Predicts device statuses (on/off), light brightness, and music type
- Special logic: If the person is sleeping or not at home, all lights are set to 0% and music is turned off

### 5. **Evaluation & Performance Tracking**
- Splits data into training and test sets
- Evaluates:
  - Device control accuracy
  - Light control mean squared error (MSE)
  - Music type prediction accuracy
- Tracks and logs model performance over time in `model_performance_history.csv`

### 6. **Input Validation**
- Ensures all inputs are within valid ranges and types before making predictions
- Provides clear error messages for invalid inputs

---

## 🛠️ How to Use

1. **Prepare your data:**
   - Ensure `smart_home_data.csv` is present in the project directory and follows the expected format.
2. **Run the model:**
   - Execute `real_model.py` as a standalone script:
     ```bash
     python real_model.py
     ```
   - The script will:
     - Analyze and display data insights
     - Train the models
     - Evaluate and print model performance
     - Make a sample prediction and print recommended actions
3. **Integrate or Extend:**
   - Use the `predict_home_automation` function to get recommendations for any context.
   - Extend the model with new features or outputs as needed!

---

## 📝 Example Prediction Output

```
Recommended Actions:
1. Turn OFF Tv Status
2. Turn OFF Smart Locks
3. Turn OFF Security Cameras
4. Turn OFF Security System
5. Turn OFF Water Heater Status
6. Set Bedroom Light brightness to 0%
7. Set Living Room Light brightness to 0%
8. Set Bathroom Light brightness to 0%
9. Set Kitchen Light brightness to 0%
10. Music: NONE (Not at home or sleeping)
```

---

## 🎨 Model Details & Design Choices

- **Random Forests** are used for robust, interpretable classification of device and music states.
- **MLP Regressor** is chosen for predicting continuous light brightness values.
- **Label Encoding** is used for categorical music types.
- **Graceful Handling of Unknowns:** The model uses string similarity and fallback defaults to handle new or misspelled input values.
- **Performance Tracking:** Every evaluation is logged for future analysis and improvement.
- **Special Rules:** Lights and music are automatically turned off when the user is sleeping or away, ensuring realistic and safe automation.

---

## 📊 Data Analysis Functions

- **analyze_data()**: Prints cross-tabs and averages for key features.
- **evaluate_models()**: Prints accuracy and error metrics for all models.
- **display_model_accuracy()**: Summarizes model performance in a user-friendly format.
- **track_model_performance()**: Logs performance metrics to CSV for tracking over time.

---

## 🧩 Extending the Project

- Add new features (e.g., weather, guest presence, energy prices)
- Integrate with real smart home APIs
- Build a web or mobile interface for real-time recommendations
- Experiment with other ML algorithms or deep learning models

---

## 💡 Inspiration & Credits

This project is inspired by the vision of a truly smart, adaptive home that understands and anticipates your needs. Built with ❤️ using Python, pandas, scikit-learn, and a passion for AI!

---

## 📬 Questions or Contributions?

Feel free to open an issue or submit a pull request. Let's make smart homes even smarter, together!

---

# 🏠✨ Enjoy your intelligent home automation journey! ✨🏠
