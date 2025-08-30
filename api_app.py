import joblib
import pandas as pd
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load the trained model and columns
model = joblib.load("pollution_model.pkl")
model_columns = joblib.load("model_columns.pkl")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        json_data = request.get_json(force=True)
        station_id = json_data['id']
        # Assuming a default year since the IoT code only sends other pollutants
        year = 2024 

        # Create a DataFrame for prediction
        input_df = pd.DataFrame({'year': [year], 'id': [station_id]})
        input_encoded = pd.get_dummies(input_df, columns=['id'])

        # Align the columns with the model's expected columns
        aligned_input = pd.DataFrame(0, index=input_encoded.index, columns=model_columns)
        for col in input_encoded.columns:
            if col in model_columns:
                aligned_input[col] = input_encoded[col]

        # Make a prediction
        prediction = model.predict(aligned_input)
        
        # Prepare the response
        pollutants = ['O2', 'NO3', 'NO2', 'SO4', 'PO4', 'CL']
        result = {p: float(val) for p, val in zip(pollutants, prediction[0])}

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)