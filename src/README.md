# Mergington High School Activities API

A super simple FastAPI application that allows students to view and sign up for extracurricular activities.

## Features

- View all available extracurricular activities
- Teachers can sign up and unregister students after logging in
- Students can view activities and current participants without logging in

## Getting Started

1. Install the dependencies:

   ```
   pip install -r requirements.txt
   ```

2. From the repository root, create a teacher account and run the application:

   ```
   python -m src.create_teacher teachername
   uvicorn src.app:app --reload
   ```

   The command prompts for a password and stores only its hash in the local
   `src/teachers.json` file. That file is ignored by Git. Set `SESSION_SECRET`
   to a persistent random value before running the app outside local
   development; set `COOKIE_SECURE=true` when serving over HTTPS.

3. Open your browser and go to:
   - API documentation: http://localhost:8000/docs
   - Alternative documentation: http://localhost:8000/redoc

## API Endpoints

| Method | Endpoint                                                          | Description                                                         |
| ------ | ----------------------------------------------------------------- | ------------------------------------------------------------------- |
| GET    | `/activities`                                                     | Get all activities with their details and current participant count |
| GET    | `/auth/session`                                                   | Check whether the current browser is logged in as a teacher          |
| POST   | `/auth/login`                                                      | Log in with a teacher username and password                         |
| POST   | `/auth/logout`                                                     | Log out                                                             |
| POST   | `/activities/{activity_name}/signup?email=student@mergington.edu` | (Teacher only) Sign up a student                                    |
| DELETE | `/activities/{activity_name}/unregister?email=student@mergington.edu` | (Teacher only) Unregister a student                              |

## Data Model

The application uses a simple data model with meaningful identifiers:

1. **Activities** - Uses activity name as identifier:

   - Description
   - Schedule
   - Maximum number of participants allowed
   - List of student emails who are signed up

2. **Students** - Uses email as identifier:
   - Name
   - Grade level

All data is stored in memory, which means data will be reset when the server restarts.
