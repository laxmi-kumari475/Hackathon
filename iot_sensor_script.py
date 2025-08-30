import requests
import json
import time
import datetime
import random # Used here to simulate sensor readings

# Configure the URL of your Flask API
# Replace 'YOUR_SERVER_IP' with the actual IP address of the computer running api_app.py
# If you are testing locally, you can use '127.0.0.1' or 'localhost'
API_URL = 'http:// 10.40.111.39:5000/predict'

def read_sensor_data(station_id):
    """
    Function to simulate reading data from water quality sensors.
    In a real-world scenario, you would replace this with actual sensor code.
    
    Args:
        station_id (str): The ID of the water monitoring station.

    Returns:
        dict: A dictionary containing the sensor readings.
    """
    print(f"Reading sensors for Station ID: {station_id}...")
    
    # Simulate a realistic range of values for pollutants
    data = {
        # Assuming your sensor collects these parameters
        # 'id' is sent with the data so the model knows which station it is
        'id': station_id,
        'O2': random.uniform(6.0, 9.5),   # Dissolved Oxygen (mg/L)
        'NO3': random.uniform(5.0, 50.0), # Nitrate (mg/L)
        'NO2': random.uniform(0.01, 3.5), # Nitrite (mg/L)
        'SO4': random.uniform(10.0, 250.0),# Sulfate (mg/L)
        'PO4': random.uniform(0.01, 0.5), # Phosphate (mg/L)
        'CL': random.uniform(15.0, 250.0)  # Chloride (mg/L)
    }
    return data

def send_data_to_api(data):
    """
    Sends the collected sensor data to the Flask API for prediction.
    
    Args:
        data (dict): The dictionary containing the sensor readings.

    Returns:
        None
    """
    try:
        # Use a POST request to send the JSON data to the API
        response = requests.post(API_URL, json=data)
        
        # Check if the request was successful
        if response.status_code == 200:
            result = response.json()
            print(f"Prediction successful at {datetime.datetime.now()}:")
            print(json.dumps(result, indent=4))
        else:
            print(f"Failed to get a prediction. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while connecting to the API: {e}")

def main():
    """Main function to run the sensor data collection and transmission loop."""
    # This is where you would define which station this device represents
    my_station_id = 'station_1' 
    
    while True:
        # 1. Read data from sensors
        sensor_data = read_sensor_data(my_station_id)
        
        # 2. Send data to the API for prediction
        send_data_to_api(sensor_data)
        
        # 3. Wait for a specified interval (e.g., 1 hour = 3600 seconds)
        print("Waiting for 1 hour before the next reading...")
        time.sleep(3600)

if __name__ == '__main__':
    main()