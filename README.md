# 🌱 EcoPlot - Smart Energy Optimization Platform

EcoPlot is a Flask-based web application designed to help users optimize their home energy consumption, reduce costs, and minimize environmental impact through AI-powered recommendations.

## 📝 Developer Note

> ### Important Setup Information:
> 
> This project already includes a configured database and a test user with the following credentials:
> - **Username/Email**: `test`
> - **Password**: `test1234`
> 
> **Do not create a new database.**
> 
> To set up your environment:
> 1. Create a Python virtual environment
> 2. Install dependencies using the provided `requirements.txt` file
> 3. If you're using the Gemini API, insert your API key into the `config.py` file by replacing `'API_KEY_HERE'`
> 
> ⚠️ **Important**: This API key is for testing purposes only. Do not commit/push your actual API key to version control.

![Screenshot 2025-05-06 223246](https://github.com/user-attachments/assets/06627a7a-760e-4cef-9505-e8f0bf2eecd5)

## ⚡ Overview

EcoPlot allows users to track and manage their home energy usage by:
- Adding and categorizing household devices with their power specifications
- Integrating renewable energy sources like solar panels and battery storage
- Receiving personalized energy optimization recommendations powered by Google's Gemini AI
- Visualizing energy consumption patterns and savings opportunities

## 🌟 Features

- **Device Management**: Track all your energy-consuming devices with detailed specifications
- **Energy Profile**: Configure your home's energy setup, including solar panels, EV chargers, and battery storage 
- **AI-Powered Recommendations**: Get personalized optimization advice based on your specific energy profile
- **Visual Dashboard**: Monitor energy usage, production, and savings through interactive charts and statistics
- **Multiple Device Categories**: Support for various device types, from appliances to EV chargers
- **Responsive Design**: Full support for both desktop and mobile views
- **Dark Mode**: Eye-friendly interface with support for light and dark themes

## 🖥️ Technology Stack

- **Backend**: Python with Flask
- **Database**: SQLAlchemy with SQLite (easily upgradable to other SQL databases)
- **Frontend**: HTML, CSS, JavaScript with Bootstrap 5
- **Charting**: Chart.js for interactive data visualization
- **AI Integration**: Google's Gemini AI API for personalized recommendations

## 🔑 Pre-configured Test Account

For testing purposes, a test user has already been configured in the database:

- **Username**: test
- **Email**: test@hotmail.com
- **Password**: test1234

## 📋 Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/EcoPlot.git
cd EcoPlot
```

### 2. Set up a virtual environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Gemini API key

Edit `EcoPlot/config.py` and replace 'API_KEY_HERE' with your Gemini API key:

```python
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY') or 'YOUR_API_KEY_HERE'
```

Alternatively, you can set it as an environment variable:

```bash
# On Windows
set GEMINI_API_KEY=your_api_key_here

# On macOS/Linux
export GEMINI_API_KEY=your_api_key_here
```

### 5. Run the application

```bash
# Navigate to the project directory if you're not already there
cd EcoPlot

# Run the app
python run.py
```

7. Access the application at `http://localhost:5000`

## ⚙️ Configuration

The application configuration is managed in the `EcoPlot/config.py` file. Key configuration options:

```python
# EcoPlot/config.py
import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the directory of the current file (config.py)
basedir = os.path.abspath(os.path.dirname(__file__))

# Create a data directory if it doesn't exist
data_dir = os.path.join(basedir, 'data')
os.makedirs(data_dir, exist_ok=True)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-for-hackathon'
    # Put the database file in the data directory
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(data_dir, 'ecoplot.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REMEMBER_COOKIE_DURATION = timedelta(days=30)
    # Gemini API config
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY') or 'YOUR_GEMINI_API_KEY'
```

For production deployment, you should set the following environment variables:
- `SECRET_KEY`: A secure random key for session encryption
- `GEMINI_API_KEY`: Your Google Gemini API key

Or

You can write gemini api key dricetly to `config.py` file `'YOUR_GEMINI_API_KEY'` section. This is just for testing don't push config file while api key written.

## 📁 Project Structure

```
EcoPlot/
├── EcoPlot/               # Application package
│   ├── __init__.py        # Application factory
│   ├── config.py          # Configuration
│   ├── forms/             # Form definitions
│   ├── models/            # Database models
│   ├── routes/            # Route handlers
│   ├── services/          # Business logic
│   ├── static/            # Static assets (CSS, JS)
│   ├── templates/         # HTML templates
│   └── seeds/             # Database seed data
├── data/                  # SQLite database file
├── requirements.txt       # Dependencies
└── run.py                 # Application entry point
```

## 🤖 Gemini AI Integration

EcoPlot uses Google's Gemini AI to generate personalized energy optimization recommendations. The integration is implemented in `EcoPlot/services/gemini_service.py`.
Gemini api key get from `https://aistudio.google.com/apikey`

To make the most of this feature:
1. Ensure you have a valid Gemini API key
2. Add multiple devices to get more personalized recommendations
3. Complete your energy profile with detailed information

## 🌐 Deployment

Contributions are welcome! Please feel free to submit a Pull Request.

## 👥 Acknowledgments

- This project was created as part of a YZTA hackathon to demonstrate sustainable energy management
- Thanks to all contributors who have helped shape this project

