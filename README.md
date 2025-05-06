# EcoPlot - Smart Energy Optimization Platform

EcoPlot is a Flask-based web application designed to help users optimize their home energy consumption, reduce costs, and minimize environmental impact through AI-powered recommendations.

## Overview

EcoPlot allows users to track and manage their home energy usage by:
- Adding and categorizing household devices with their power specifications
- Integrating renewable energy sources like solar panels and battery storage
- Receiving personalized energy optimization recommendations powered by Google's Gemini AI
- Visualizing energy consumption patterns and savings opportunities

## Features

- **Device Management**: Track all your energy-consuming devices with detailed specifications
- **Energy Profile**: Configure your home's energy setup, including solar panels, EV chargers, and battery storage 
- **AI-Powered Recommendations**: Get personalized optimization advice based on your specific energy profile
- **Visual Dashboard**: Monitor energy usage, production, and savings through interactive charts and statistics
- **Multiple Device Categories**: Support for various device types, from appliances to EV chargers
- **Responsive Design**: Full support for both desktop and mobile views
- **Dark Mode**: Eye-friendly interface with support for light and dark themes

## Technology Stack

- **Backend**: Python with Flask
- **Database**: SQLAlchemy with SQLite (easily upgradable to other SQL databases)
- **Frontend**: HTML, CSS, JavaScript with Bootstrap 5
- **Charting**: Chart.js for interactive data visualization
- **AI Integration**: Google's Gemini AI API for personalized recommendations

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/EcoPlot.git
cd EcoPlot
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

4. Configure your Gemini API key:
- Get a Gemini API key from [Google AI Studio](https://ai.google.dev/)
- Create a `.env` file in the project root directory
- Add your API key to the `.env` file:
```
GEMINI_API_KEY=your_api_key_here
```

5. Initialize the database:
```bash
flask shell
```
```python
from EcoPlot import db, create_app
from EcoPlot.seeds.seed_devices import seed_device_types_and_brands
app = create_app()
with app.app_context():
    db.create_all()
    seed_device_types_and_brands()  # Seed the database with device types and brands
```

6. Run the application:
```bash
flask run
```

7. Access the application at `http://localhost:5000`

## Configuration

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
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
```

For production deployment, you should set the following environment variables:
- `SECRET_KEY`: A secure random key for session encryption
- `GEMINI_API_KEY`: Your Google Gemini API key

## Project Structure

```
EcoPlot/
├── EcoPlot/              # Main application package
│   ├── __init__.py       # App initialization
│   ├── config.py         # Configuration
│   ├── forms/            # Form definitions
│   ├── models/           # Database models
│   ├── routes/           # Route definitions
│   ├── services/         # Business logic
│   ├── static/           # Static assets (CSS, JS)
│   ├── templates/        # HTML templates
│   └── seeds/            # Database seed data
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

## Gemini AI Integration

EcoPlot uses Google's Gemini AI to generate personalized energy optimization recommendations. The integration is implemented in `EcoPlot/services/gemini_service.py`.

To make the most of this feature:
1. Ensure you have a valid Gemini API key
2. Add multiple devices to get more personalized recommendations
3. Complete your energy profile with detailed information

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- This project was created as part of a hackathon to demonstrate sustainable energy management
- Thanks to all contributors who have helped shape this project
