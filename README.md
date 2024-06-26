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
- Python 3.12+
- PostgreSQL 16+ (We highly recomend using an UNIX machine, or MACOS)
  - https://www.moncefbelyamani.com/how-to-install-postgresql-on-a-mac-with-homebrew-and-lunchy/ 
  - https://www.geeksforgeeks.org/install-postgresql-on-windows/
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
   - To get the Google_maps_api_key, use the google places api.
   - To get the huggingface token, go to the huggingface website, sign up for a token and allow for read/write. 
   - Create a `.env` file in the project root directory and add the following environment variables with your credentials:
     ```plaintext
     SOCIAL_AUTH_GOOGLE_CLIENT_ID = "your_google_client_id"
     SOCIAL_AUTH_GOOGLE_SECRET = "your_google_secret"
     GOOGLE_MAPS_API_KEY = "your_google_maps_api_key"
     HF_TOKEN = "your_hugging_face_token"
     ```
   - Create a PostgreSQL database named `resumeAI` with a user `core`:
     ```sql
     CREATE DATABASE resumeai;
     CREATE USER core WITH PASSWORD 'password';
     GRANT ALL PRIVILEGES ON DATABASE resumeai TO core;
     ```
   - Initialize and migrate the database schema. If there is anything in the migrations folders, remove everything but the _init_.py:
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

## LINKS TO VIDEOS:
- Employer Perspective
  - https://www.youtube.com/watch?v=B7x744DQD6A
- JobSearcher Perspective
  - https://www.youtube.com/watch?v=quuw8BRcraQ

## LINKS TO TEST RESUMES:
https://drive.google.com/drive/folders/1bwZn02UFOwsGK_km0bRaL-vbKAzZF6kW?usp=sharing
- blank.pdf only for create-resume test!
