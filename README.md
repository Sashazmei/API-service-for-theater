# API-service-for-theater 🎭

This is a REST API service for managing a theater system, built using Django and Django REST Framework.

## 🔧 Features

- Create and view plays
- Actors and genres management
- Performance sessions
- Seat reservations and ticketing
- JWT authentication
- Swagger documentation (drf-spectacular)

## 🚀 How to Run

```bash
git clone https://github.com/Sashazmei/API-service-for-theater.git
cd API-service-for-theater

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Run the server
python manage.py runserver
