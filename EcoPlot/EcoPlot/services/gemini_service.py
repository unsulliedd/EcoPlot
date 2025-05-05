# EcoPlot/services/gemini_service.py
import os
import json
from flask import current_app
from google import genai

class GeminiService:
    """
    Service class for interacting with Google's Gemini API to generate
    personalized energy optimization recommendations.
    """
    def __init__(self):
        """Initialize the Gemini API client with API key from app config."""
        # Get API key from Flask app configuration
        api_key = current_app.config.get('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("Gemini API key not found in configuration")

        # Initialize the Gemini client with the API key directly
        self.client = genai.Client(api_key=api_key)
        # Use the Gemini flash model for efficient responses
        self.model_name = "gemini-2.0-flash-001"

    def generate_device_recommendations(self, user_data, devices_data):
        """
        Generate personalized recommendations for device usage optimization.

        Args:
            user_data (dict): User preferences and energy setup details
            devices_data (list): List of user's devices with their specifications

        Returns:
            dict: Structured recommendations or error message
        """
        try:
            # Create the prompt for Gemini API
            prompt = self._create_recommendation_prompt(user_data, devices_data)
            
            # Generate content using Gemini API through the models interface
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            
            # Parse the response to extract structured recommendations
            return self._parse_recommendations(response.text)
        except Exception as e:
            print(f"Error generating recommendations: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "recommendations": []
            }

    def _create_recommendation_prompt(self, user_data, devices_data):
        """
        Create a detailed prompt for Gemini to generate energy optimization recommendations.
        
        Args:
            user_data (dict): User preferences and energy setup
            devices_data (list): User's devices information
            
        Returns:
            str: Formatted prompt for Gemini API
        """
        # Format devices data for the prompt
        devices_text = ""
        for device in devices_data:
            device_info = (
                f"- {device.get('name', 'Unknown Device')} ({device.get('device_type_name', 'Unknown Type')}):\n"
                f"  - ID: {device.get('id', 'Unknown')}\n"
                f"  - Brand: {device.get('brand_name', 'Unknown')}\n"
                f"  - Power Consumption: {device.get('power_consumption_watts', 0)}W\n"
            )
            
            # Add optional device details if available
            if device.get('standby_power_watts') is not None:
                device_info += f"  - Standby Power: {device.get('standby_power_watts')}W\n"
            
            if device.get('average_usage_hours_per_day') is not None:
                device_info += f"  - Average Daily Usage: {device.get('average_usage_hours_per_day')} hours/day\n"
            
            if device.get('usage_flexibility') is not None:
                device_info += f"  - Usage Flexibility: {device.get('usage_flexibility')}/10\n"
            
            # Add flags for special device types
            flags = []
            if device.get('is_schedulable'):
                flags.append("Schedulable")
            if device.get('is_smart_device'):
                flags.append("Smart Device")
            if device.get('is_ev_charger'):
                flags.append("EV Charger")
                
            if flags:
                device_info += f"  - Features: {', '.join(flags)}\n"
                
            devices_text += device_info + "\n"

        # Safeguard missing user data with default values
        location = user_data.get('location', user_data.get('city', 'Unknown'))
        has_solar = user_data.get('has_solar', False)
        solar_capacity = user_data.get('solar_capacity_kw', 0) if has_solar else 0
        has_battery = user_data.get('has_battery_storage', False)
        battery_capacity = user_data.get('battery_capacity_kwh', 0) if has_battery else 0
        
        # Build the complete prompt for Gemini
        prompt = f"""
        You are an energy optimization expert for the EcoPlot application.
        Your task is to analyze user data and device information to create personalized
        recommendations for optimizing energy usage, reducing costs, and minimizing
        environmental impact.

        ## User Information:
        - Location: {location}
        - Has Solar Panels: {has_solar}
        - Solar Capacity: {solar_capacity} kW
        - Solar Panel Orientation: {user_data.get('solar_panel_orientation', 'Unknown')}
        - Has Battery Storage: {has_battery}
        - Battery Capacity: {battery_capacity} kWh
        - Has Electric Vehicle: {user_data.get('has_ev', False)}
        - Electricity Rate Plan: {user_data.get('electricity_rate_plan', 'Unknown')}
        - Peak Rate: ${user_data.get('peak_rate_per_kwh', 0)}/kWh
        - Off-peak Rate: ${user_data.get('off_peak_rate_per_kwh', 0)}/kWh
        - Energy Savings Goal: {user_data.get('energy_savings_goal', 0)}%
        - Environmental Priority: {user_data.get('environmental_priority', 5)}/10

        ## Devices Information:
        {devices_text}

        Based on this information, provide comprehensive energy optimization recommendations
        in the following JSON format. Make sure all your recommendations are practical,
        specific, and tailored to the user's situation:

        ```json
        {{
          "overall_recommendations": [
            "Install a smart energy management system",
            "Shift high-consumption activities to off-peak hours",
            "Consider upgrading to more energy-efficient devices"
          ],
          "device_recommendations": {{
            "device_id_1": {{
              "name": "Device Name",
              "recommendation": "Specific optimization advice for this device",
              "estimated_savings": 5.2
            }},
            "device_id_2": {{
              "name": "Another Device",
              "recommendation": "Specific optimization advice for this device",
              "estimated_savings": 3.8
            }}
          }},
          "schedule_optimization": [
            "Charge EV between 10 AM and 3 PM to utilize solar production",
            "Run dishwasher after 9 PM to utilize off-peak rates",
            "Schedule washing machine for weekends when home energy demand is lower"
          ],
          "energy_saving_tips": [
            "Turn off devices completely instead of leaving them on standby",
            "Use natural light during the day instead of artificial lighting",
            "Keep air conditioning filters clean to improve efficiency"
          ],
          "estimated_monthly_savings": 45.80,
          "carbon_reduction_potential": 32.5
        }}
        ```

        Ensure that:
        1. All recommendations are realistic and specific
        2. Device recommendations reference actual device IDs from the provided data
        3. Estimated savings are realistic and based on device power consumption
        4. If the user has solar, include recommendations to align usage with solar production
        5. Consider the user's electricity rate plan when suggesting scheduling
        6. Only respond with valid JSON that follows the exact structure shown above
        """

        return prompt

    def _parse_recommendations(self, response_text):
        """
        Parse the Gemini API response to extract structured recommendations.
        
        Args:
            response_text (str): Raw text response from Gemini API
            
        Returns:
            dict: Parsed recommendations or error message
        """
        try:
            # Extract JSON content from the response using code block markers
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_text = response_text[json_start:json_end]
                recommendations = json.loads(json_text)
                
                # Validate the required fields
                required_fields = [
                    'overall_recommendations', 
                    'device_recommendations', 
                    'schedule_optimization', 
                    'energy_saving_tips'
                ]
                
                for field in required_fields:
                    if field not in recommendations:
                        recommendations[field] = []
                
                # Ensure numeric fields are present
                if 'estimated_monthly_savings' not in recommendations:
                    recommendations['estimated_monthly_savings'] = 0
                    
                if 'carbon_reduction_potential' not in recommendations:
                    recommendations['carbon_reduction_potential'] = 0
                
                return {
                    "success": True,
                    "recommendations": recommendations
                }
            else:
                raise ValueError("No valid JSON structure found in response")
        except json.JSONDecodeError as e:
            print(f"JSON parse error: {str(e)}")
            print(f"Response text: {response_text}")
            return {
                "success": False,
                "error": f"Could not parse recommendations: {str(e)}",
                "raw_response": response_text
            }
        except Exception as e:
            print(f"Error parsing recommendations: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }