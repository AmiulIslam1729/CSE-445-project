# rice_yield_predictor.py
# This file serves as a bridge between the Streamlit frontend and the backend model

import pandas as pd
import numpy as np
import pickle
import os
import warnings
warnings.filterwarnings('ignore')

class RiceYieldPredictor:
    def __init__(self, model_path='rice_yield_model.pkl', 
                 region_encoder_path='region_encoder.pkl',
                 rice_types_path='rice_types.pkl'):
        """
        Initialize the predictor by loading the model and necessary components
        """
        # Check if files exist
        self._check_files_exist([model_path, region_encoder_path, rice_types_path])
        
        # Load the model and components
        try:
            with open(model_path, 'rb') as f:
                self.model = pickle.load(f)
                
            with open(region_encoder_path, 'rb') as f:
                self.region_encoder = pickle.load(f)
                
            with open(rice_types_path, 'rb') as f:
                self.rice_types = pickle.load(f)
                
            print("Model and components loaded successfully!")

            # Monthly weather data
            self.monthly_weather_data = {
                'January': {'Temperature (°C)': 18.6, 'Humidity (Percent)': 65, 'Rainfall (mm)': 8},
                'February': {'Temperature (°C)': 21.3, 'Humidity (Percent)': 60, 'Rainfall (mm)': 20},
                'March': {'Temperature (°C)': 25.0, 'Humidity (Percent)': 61, 'Rainfall (mm)': 40},
                'April': {'Temperature (°C)': 28.4, 'Humidity (Percent)': 66, 'Rainfall (mm)': 100},
                'May': {'Temperature (°C)': 29.5, 'Humidity (Percent)': 73, 'Rainfall (mm)': 200},
                'June': {'Temperature (°C)': 29.0, 'Humidity (Percent)': 78, 'Rainfall (mm)': 300},
                'July': {'Temperature (°C)': 28.9, 'Humidity (Percent)': 80, 'Rainfall (mm)': 504},
                'August': {'Temperature (°C)': 29.0, 'Humidity (Percent)': 80, 'Rainfall (mm)': 337},
                'September': {'Temperature (°C)': 28.8, 'Humidity (Percent)': 79, 'Rainfall (mm)': 250},
                'October': {'Temperature (°C)': 27.5, 'Humidity (Percent)': 74, 'Rainfall (mm)': 150},
                'November': {'Temperature (°C)': 24.0, 'Humidity (Percent)': 70, 'Rainfall (mm)': 50},
                'December': {'Temperature (°C)': 20.0, 'Humidity (Percent)': 68, 'Rainfall (mm)': 10},
            }

            # Define rice-type-specific weather averaging months
            self.rice_type_months = {
                'Amon Broadcast': ['March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
                'Amon HYV': ['June', 'July', 'August', 'September', 'October', 'November', 'December'],
                'Amon L.T': ['June', 'July', 'August', 'September', 'October', 'November', 'December'],
                'Aus HYV': ['March', 'April', 'May', 'June', 'July', 'August'],
                'Aus Local': ['March', 'April', 'May', 'June', 'July', 'August'],
                'Boro HYV': ['January', 'February', 'March', 'April', 'May', 'June'],
                'Boro Hybrid': ['January', 'February', 'March', 'April', 'May', 'June'],
                'Boro Local': ['January', 'February', 'March', 'April', 'May']
            }

        except Exception as e:
            raise RuntimeError(f"Error loading model components: {str(e)}")
    
    def _check_files_exist(self, file_paths):
        """Check if required files exist"""
        missing_files = [f for f in file_paths if not os.path.exists(f)]
        if missing_files:
            raise FileNotFoundError(f"Required model files not found: {', '.join(missing_files)}")
    
    def predict(self, region, rice_type, area_size):
        """
        Make a yield prediction based on input parameters
        """
        try:
            # Validate inputs
            if region not in self.region_encoder.classes_:
                raise ValueError(f"Region '{region}' not in training data")
            
            if rice_type not in self.rice_types:
                raise ValueError(f"Rice type '{rice_type}' not in training data")

            # Calculate weather data based on rice type
            months = self.rice_type_months.get(rice_type, list(self.monthly_weather_data.keys()))
            temps = [self.monthly_weather_data[month]['Temperature (°C)'] for month in months]
            rains = [self.monthly_weather_data[month]['Rainfall (mm)'] for month in months]
            hums = [self.monthly_weather_data[month]['Humidity (Percent)'] for month in months]
            avg_temp = sum(temps) / len(temps)
            avg_rain = sum(rains) / len(rains)
            avg_hum = sum(hums) / len(hums)

            # Create input DataFrame for prediction
            input_data = pd.DataFrame({
                'Year': [2024],
                'Region': [region],
                'Rice Type': [rice_type],
                'Area (Hectare)': [float(area_size)],
                'Temperature (°C)': [avg_temp],
                'Rainfall (mm)': [avg_rain],
                'Humidity (Percent)': [avg_hum]
            })

            # Make prediction
            prediction = self.model.predict(input_data)[0]
            
            # Handle NaN predictions (if any)
            if np.isnan(prediction):
                prediction = 5.5  # Default fallback value
            
            # Calculate yield per hectare and total yield
            yield_per_hectare = prediction / float(area_size)
            total_yield = prediction
            
            yield_per_hectare = round(yield_per_hectare, 2)
            total_yield = round(total_yield, 2)
            
            return {
                'yield_per_hectare': yield_per_hectare,
                'total_yield': total_yield
            }
            
        except Exception as e:
            print(f"Error during prediction: {str(e)}")
            return {
                'error': str(e),
                'yield_per_hectare': 0.0,
                'total_yield': 0.0
            }
    
    def get_regions(self):
        """Return the list of available regions"""
        return sorted(list(self.region_encoder.classes_))
    
    def get_rice_types(self):
        """Return the list of available rice types"""
        return sorted(self.rice_types)

# Testing the predictor
if __name__ == "__main__":
    try:
        predictor = RiceYieldPredictor()
        
        test_region = predictor.get_regions()[0]
        test_rice_type = predictor.get_rice_types()[0]
        test_area = 2.5
        
        result = predictor.predict(test_region, test_rice_type, test_area)
        
        print(f"Test prediction for {test_rice_type} in {test_region} with area {test_area} hectares:")
        print(f"Yield per hectare: {result['yield_per_hectare']} tons")
        print(f"Total yield: {result['total_yield']} tons")
        
    except Exception as e:
        print(f"Error testing predictor: {str(e)}")
