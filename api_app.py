import joblib
import pandas as pd
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load the trained model and columns
try:
    model = joblib.load("pollution_model.pkl")
    model_columns = joblib.load("model_columns.pkl")
    # --- Filter out the 'year' column to get only the station IDs ---
    known_station_ids = [col.replace('id_', '') for col in model_columns if col.startswith('id_')]
except FileNotFoundError:
    print("Error: Model files not found. Ensure 'pollution_model.pkl' and 'model_columns.pkl' are in the directory.")
    # Exit or handle gracefully if critical files are missing
    exit()

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # The API now expects JSON with 'id' and 'year'
        json_data = request.get_json(force=True)
        station_id = str(json_data.get('id'))
        year_input = int(json_data.get('year'))

        # Check if the station ID is valid
        if station_id not in known_station_ids:
            return jsonify({'error': f"Station ID '{station_id}' is not known to the model."}), 400

        # Create a DataFrame for prediction
        input_df = pd.DataFrame({'year': [year_input], 'id': [station_id]})
        input_encoded = pd.get_dummies(input_df, columns=['id'], prefix='id')

        # Align the columns with the model's expected columns
        # This is a more robust way to ensure the columns match
        aligned_input = pd.DataFrame(0, index=[0], columns=model_columns)
        for col in aligned_input.columns:
            if col in input_encoded.columns:
                aligned_input[col] = input_encoded[col].iloc[0]

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
