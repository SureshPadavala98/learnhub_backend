# Stepupmark Learn Hub Backend

Backend API for Stepupmark Learn Hub.

## Tech Stack

- Django
- Django REST Framework
- PostgreSQL
- JWT Authentication

## Setup

### Clone

git clone <repo-url>

### Create Virtual Environment

python -m venv venv

### Activate

source venv/bin/activate

### Install Dependencies

pip install -r requirements.txt

### Create Environment Variables

cp .env.example .env

### Run Migrations

python manage.py migrate

### Start Server

python manage.py runserver