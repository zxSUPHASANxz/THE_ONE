# THE_ONE - Motorcycle Repair Chatbot & Booking System

A professional web application for motorcycle symptom assessment, repair assistance, and appointment booking system with integrated AI chatbot powered by n8n.

## Features

- 🤖 **AI Chatbot**: Intelligent chatbot for motorcycle symptom assessment and repair guidance
- 🏍️ **Big Bike Support**: Support for motorcycles 150cc and above, including all big bike models
- 📅 **Booking System**: Easy appointment scheduling for repairs
- 👨‍🔧 **Mechanic Dashboard**: Queue management and repair status updates
- 🔍 **Web Scraping**: Automated data collection from trusted sources and Pantip
- 📊 **RAG System**: Retrieval-Augmented Generation for accurate answers

## Tech Stack

- **Backend**: Django 5.0, Django REST Framework
- **Frontend**: TailwindCSS, Alpine.js, htmx
- **Database**: PostgreSQL
- **Automation**: n8n (Docker)
- **Tunneling**: ngrok
- **Deployment**: Docker, Gunicorn

## Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Docker & Docker Compose
- Node.js 18+ (for TailwindCSS)
- ngrok account

## Installation

### 1. Clone the repository
```bash
cd d:\Project\THE_ONE_V4
```

### 2. Create virtual environment
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup environment variables
```bash
copy .env.example .env
# Edit .env with your configuration
```

### 5. Setup PostgreSQL
```bash
# Create database
createdb the_one_db
```

### 6. Run migrations
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 7. Install TailwindCSS
```bash
npm install
npm run tailwind:build
```

### 8. Start n8n with Docker
```bash
docker-compose up -d
```

### 9. Run the development server
```bash
python manage.py runserver
```

## Project Structure

```
THE_ONE_V4/
├── the_one/                 # Django project
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── chatbot/            # Chatbot app
│   ├── booking/            # Booking system app
│   ├── users/              # User management
│   └── mechanics/          # Mechanic dashboard
├── static/                 # Static files
├── templates/              # HTML templates
├── docker-compose.yml      # Docker configuration
├── requirements.txt
└── README.md
```

## Usage

1. Access the application at `http://localhost:8000`
2. Access n8n at `http://localhost:5678`
3. Access Django admin at `http://localhost:8000/admin`

## API Endpoints

- `/api/chat/` - Chatbot endpoints
- `/api/bookings/` - Booking management
- `/api/mechanics/` - Mechanic queue management
- `/api/webhooks/n8n/` - n8n webhook integration

## Contributing

This is a private project for motorcycle repair services.

## License

Proprietary - All rights reserved
