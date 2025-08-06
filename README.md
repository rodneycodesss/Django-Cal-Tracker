# Calorie Tracker

A modern web application built with Django and Tailwind CSS for tracking daily calorie consumption. This application allows users to add food items, track their daily calorie intake, and maintain a personal food database.

## Features

### Core Functionality
- **Calorie Tracking**: Add new food items with their respective calorie count
- **Food Database**: View a list of all food items added so far
- **Daily Management**: Remove food items from the daily list
- **Calorie Calculation**: Calculate and display the total number of calories consumed for the day
- **Reset Functionality**: Reset the calorie count for the day

### User Interface
- **Responsive Design**: Modern, mobile-friendly interface using Tailwind CSS
- **User Authentication**: Secure login and registration system
- **Dashboard**: Comprehensive overview of daily calorie consumption
- **Food Management**: Easy-to-use interface for managing food items

### Technical Features
- **Database**: PostgreSQL for production, SQLite for development
- **Security**: Django best practices for data validation and security
- **Performance**: Optimized queries and efficient data handling
- **Deployment Ready**: Configured for easy deployment on platforms like Render

## Technology Stack

- **Backend**: Django 4.2+
- **Frontend**: HTML5, CSS3, Tailwind CSS
- **Database**: PostgreSQL (production), SQLite (development)
- **Authentication**: Django's built-in user authentication
- **Deployment**: Gunicorn, WhiteNoise for static files

## Installation and Setup

### Prerequisites
- Python 3.8 or higher
- PostgreSQL (for production)
- Git

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Django-Cal-Tracker
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

5. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   Open your browser and navigate to `http://127.0.0.1:8000`

### Production Setup

1. **Set up PostgreSQL database**
   - Create a PostgreSQL database
   - Note the database URL for configuration

2. **Configure environment variables**
   ```env
   SECRET_KEY=your-production-secret-key
   DEBUG=False
   ALLOWED_HOSTS=your-domain.com,www.your-domain.com
   DATABASE_URL=postgresql://username:password@host:port/database_name
   ```

3. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

## Usage

### Getting Started
1. Register a new account or log in with existing credentials
2. Add food items to your personal database
3. Track your daily calorie consumption by adding food entries
4. Monitor your progress on the dashboard
5. Reset your daily count when needed

### Adding Food Items
1. Navigate to "Add Food" from the navigation menu
2. Enter the food name, calories per serving, and serving size
3. Save the food item to your database

### Tracking Daily Calories
1. From the dashboard, click "Add Food" to log a food entry
2. Select a food item from your database
3. Enter the quantity consumed
4. The system automatically calculates and updates your daily total

### Managing Your Data
- View all your food items in the "Foods" section
- Delete individual food entries from your daily log
- Reset your daily calorie count when starting a new day

## Project Structure

```
Django-Cal-Tracker/
├── calorie_tracker/          # Main Django project
│   ├── settings.py          # Project settings
│   ├── urls.py              # Main URL configuration
│   └── wsgi.py              # WSGI configuration
├── tracker/                 # Main Django app
│   ├── models.py            # Database models
│   ├── views.py             # View functions
│   ├── urls.py              # App URL configuration
│   ├── forms.py             # Django forms
│   └── admin.py             # Admin interface
├── templates/               # HTML templates
│   └── tracker/             # App-specific templates
├── static/                  # Static files (CSS, JS, images)
├── requirements.txt         # Python dependencies
├── Procfile                 # Deployment configuration
└── README.md               # This file
```

## Database Models

### FoodItem
- Stores food items with calorie information
- Fields: name, calories, serving_size, timestamps

### DailyCalorieLog
- Tracks daily calorie consumption
- Fields: user, date, total_calories, timestamps

### CalorieEntry
- Individual food entries for each day
- Fields: daily_log, food_item, quantity, calories_consumed, notes


## Security Considerations

- Django's built-in security features are enabled
- CSRF protection is active
- SQL injection protection through Django ORM
- XSS protection through template escaping
- Secure password hashing
- Environment variables for sensitive data
