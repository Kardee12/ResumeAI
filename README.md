# ResumeAI
**Connecting New Graduates and Employers**

## Table of Contents
- [Introduction](#introduction)
- [System Requirements](#system-requirements)
  - [Production Environment](#production-environment)
  - [Development Environment](#development-environment)
- [Team](#team)

## Introduction
**ResumeAI** is a comprehensive web application designed to facilitate connections between new graduates seeking job opportunities and employers looking for fresh talent. 

**Technology Stack:**
- **Frontend:** HTML, CSS, Bootstrap, Javascript
- **Backend:** Django
- **Database:** PostgreSQL
- **APIs:** Hugging Face, Google Maps Places API

## System Requirements
- Python 3.8+
- PostgreSQL 10+

### Production Environment
To set up ResumeAI in a production environment, follow these steps:

1. **Environment Setup:**
   - Create a virtual environment:
     ```bash
     python -m venv venv
     ```
   - Activate the virtual environment and install dependencies:
     ```bash
     source venv/bin/activate  # On Windows use `venv\Scripts\activate`
     pip install -r requirements.txt
     ```

2. **Configuration:**
   - Create your own API credentials for Google and Hugging Face. Store these securely.
   - Create a `.env` file in the project root directory and add the following environment variables with your credentials:
     ```plaintext
     SOCIAL_AUTH_GOOGLE_CLIENT_ID = "your_google_client_id"
     SOCIAL_AUTH_GOOGLE_SECRET = "your_google_secret"
     GOOGLE_MAPS_API_KEY = "your_google_maps_api_key"
     HF_TOKEN = "your_hugging_face_token"
     ```
   - Create a PostgreSQL database named `resumeAI` with a user `core`:
     ```sql
     CREATE DATABASE resumeAI;
     CREATE USER core WITH PASSWORD 'password';
     GRANT ALL PRIVILEGES ON DATABASE resumeAI TO core;
     ```
   - Initialize and migrate the database schema:
     ```bash
     python manage.py makemigrations
     python manage.py migrate
     ```

3. **Run the Application:**
   - Start the Django server:
     ```bash
     python manage.py runserver
     ```
   - Access the application at: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

### Development Environment
Ensure the PostgreSQL database is active, and API credentials are up to date before starting the development server:
```bash
python manage.py runserver
```

## Authors
- [@IbrahimD0](https://github.com/Ibrahimd0)
- [@Kardee12](https://github.com/Kardee12)
- [@jrveloya](https://github.com/jrveloya)
- [@ShunF0712](https://github.com/ShunF0712)
- [@mich-thy](https://github.com/mich-thy)
