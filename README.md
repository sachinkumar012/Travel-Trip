# Travel Trip - Tour and Travel Booking System

A comprehensive Django-based web application for booking flights, hotels, and travel packages. This platform allows users to search, compare, and book travel services with an intuitive interface and complete booking management system.

## Features

### 🎯 Core Functionality
- **Flight Booking**: Search and book flights with real-time availability checking
- **Hotel Booking**: Browse hotels by city with detailed information and ratings
- **Package Booking**: Create customized travel packages combining flights and hotels
- **Places Explorer**: Discover famous places and tourist destinations

### 👤 User Features
- **User Authentication**: Secure registration and login system
- **My Booking Dashboard**: 
  - View all bookings (Flights, Hotels, Packages)
  - View detailed booking information
  - Manage multiple passengers for bookings
  - Cancel bookings
- **Passenger Management**: 
  - Fill passenger details before confirmation
  - Manage individual passenger information for multiple seats/rooms
  - Store passenger contact and ID information

### 🎨 User Interface
- Modern, responsive design with gradient backgrounds
- Beautiful card-based layouts
- Intuitive navigation
- Mobile-friendly interface

## Technology Stack

- **Backend**: Django 5.2.4
- **Database**: SQLite3
- **Frontend**: HTML, CSS, Bootstrap 4.4.1
- **Icons**: Ionicons
- **Image Processing**: Pillow

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Tour-And-Travel-Django-App
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser (optional, for admin access)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Open your browser and navigate to `http://127.0.0.1:8000/`
   - Admin panel: `http://127.0.0.1:8000/admin/`

## Project Structure

```
Tour-And-Travel-Django-App/
├── manage.py
├── requirements.txt
├── db.sqlite3
├── tourAndTravel/          # Main project settings
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── travelapp/              # Main application
│   ├── models.py           # Database models
│   ├── views.py            # View functions
│   ├── forms.py            # Form definitions
│   ├── urls.py             # URL routing
│   ├── admin.py            # Admin configuration
│   └── migrations/         # Database migrations
├── templates/              # HTML templates
│   ├── index.html
│   ├── dashboard.html
│   ├── flights.html
│   ├── hotels.html
│   ├── package.html
│   ├── bookflight.html
│   ├── bookhotel.html
│   ├── bookpackage.html
│   ├── confirmflight.html
│   ├── confirmhotel.html
│   ├── confirmpackage.html
│   ├── viewbooking.html
│   ├── managepassengers.html
│   └── registration/
├── static/                 # Static files
│   ├── css/
│   └── img/
└── media/                  # User uploaded files
    └── img/
```

## Database Models

### Core Models
- **City**: Stores city information
- **Flights**: Flight details and availability
- **Hotels**: Hotel information and pricing
- **Famous**: Famous places and tourist destinations

### Booking Models
- **BookFlight**: Flight bookings with passenger details
- **BookHotel**: Hotel bookings with guest details
- **BookPackage**: Package bookings combining flights and hotels
- **Passenger**: Individual passenger details for multiple bookings

## Usage Guide

### For Users

1. **Registration/Login**
   - Click "REGISTER" to create a new account
   - Or "LOGIN" if you already have an account

2. **Search Flights**
   - Navigate to "FLIGHTS"
   - Enter source, destination, and date
   - View available flights and book

3. **Search Hotels**
   - Navigate to "HOTELS"
   - Enter city and date
   - Browse hotels and make reservations

4. **Book Packages**
   - Navigate to "PACKAGES"
   - Enter source, destination, and date
   - Select flight and hotel
   - Complete booking with passenger details

5. **Manage Bookings**
   - Go to "MY BOOKING" dashboard
   - View all your bookings
   - Click "VIEW" to see detailed information
   - Click "PASSENGERS/GUESTS" to manage multiple passengers
   - Cancel bookings if needed

### For Administrators

1. **Access Admin Panel**
   - Navigate to `/admin/`
   - Login with superuser credentials

2. **Manage Data**
   - Add/edit flights, hotels, cities, and places
   - View and manage user bookings
   - Monitor passenger information

## Key Features Explained

### Passenger Details Management
- When booking multiple seats/rooms, users can fill details for each passenger separately
- Primary passenger details are stored in the booking model
- Additional passengers are stored in the Passenger model
- All passenger information is accessible from the booking details page

### Booking Confirmation Flow
1. User selects flight/hotel/package
2. User enters number of seats/rooms
3. User is redirected to confirmation page
4. User fills passenger details form
5. Booking is confirmed and saved
6. User can view and manage booking from dashboard

## Configuration

### Settings
Key settings in `tourAndTravel/settings.py`:
- `DEBUG = True` (set to False in production)
- `ALLOWED_HOSTS = []` (add your domain in production)
- `DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'`
- Static and media files configuration

### Database
- Default: SQLite3 (development)
- For production, configure PostgreSQL or MySQL in settings.py

## Development

### Running Tests
```bash
python manage.py test
```

### Creating Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Collecting Static Files
```bash
python manage.py collectstatic
```

## Production Deployment

1. Set `DEBUG = False` in settings.py
2. Add your domain to `ALLOWED_HOSTS`
3. Configure a production database (PostgreSQL recommended)
4. Set up static file serving (WhiteNoise or CDN)
5. Configure media file storage
6. Set up environment variables for sensitive data
7. Use a production WSGI server (Gunicorn, uWSGI)
8. Set up reverse proxy (Nginx)

## Security Notes

- Never commit `SECRET_KEY` or sensitive credentials
- Use environment variables for sensitive configuration
- Keep dependencies updated
- Use HTTPS in production
- Implement proper authentication and authorization

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is open source and available for educational purposes.

## Support

For issues or questions, please open an issue in the repository.

## Recent Updates

- ✅ Added passenger details form before booking confirmation
- ✅ Implemented multiple passenger management for bookings
- ✅ Added "View Details" functionality for all bookings
- ✅ Enhanced dashboard with better navigation
- ✅ Improved About Us section with aesthetic design
- ✅ Fixed template syntax errors
- ✅ Updated models to support passenger information
- ✅ Added comprehensive booking details view

## Author

Travel Trip Development Team

---

**Note**: This is a development version. For production use, ensure proper security measures, database configuration, and deployment setup.


