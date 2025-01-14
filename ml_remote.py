from flask import Flask, request, jsonify
import joblib
import pandas as pd

# Cargar el modelo
model = joblib.load("rf_model.pkl")

feature_names = [
    'freq_count_1', 'rssi_count_1', 'rssi_max_1', 'rssi_min_1', 'rssi_spread_1', 'rssi_stdev_1',
    'freq_count_2', 'rssi_count_2', 'rssi_max_2', 'rssi_min_2', 'rssi_spread_2', 'rssi_stdev_2'
]
class_names = model.classes_

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    features = {feature: data.get(feature, 0.0) for feature in feature_names}
    df = pd.DataFrame([features])
    print(df)
    prediction = model.predict_proba(df)
    probas_dict = {class_names[i]: prob for i, prob in enumerate(prediction[0])}
    print(probas_dict)
    return jsonify({'prediction': probas_dict})

# Response Json
# {
#   "prediction": {
#     "far": 0.21,
#     "med": 0.66,
#     "near": 0.13
#   }
# }

if __name__ == "__main__":
    app.run(debug=True)
