# Aceest Fitness Gym 2024 (TM93112)

## Description
Aceest Fitness Gym 2024 is a Flask-based web application designed to help users track workouts, manage gym memberships, and analyze fitness progress. This project provides a robust backend with RESTful APIs and supports containerized deployment and automated testing.

## Local Setup
Follow these steps to set up the project locally:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/IMRaghvendraMishra/aceest-fitness-gym-2024tm93112.git
   cd aceest-fitness-gym-2024tm93112
   ```
2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the Flask app:**
   ```bash
   python src/app.py
   ```

## Running Tests
To run the test suite using pytest:
```bash
pytest
```

## Docker Instructions
To build and run the application using Docker:

1. **Build the Docker image:**
   ```bash
   docker build -t fitness-app .
   ```
2. **Run the Docker container:**
   ```bash
   docker run -p 5000:5000 fitness-app
   ```

## CI/CD Workflow
This project uses GitHub Actions for CI/CD. The workflow performs the following steps:

1. **Install dependencies:** Sets up Python and installs all required packages.
2. **Run tests:** Executes the test suite using pytest to ensure code quality.
3. **Build Docker image:** Builds the Docker image to verify containerization works as expected.

All steps are automated and triggered on push and pull request events to the main branch.
