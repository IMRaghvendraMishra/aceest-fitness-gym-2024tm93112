# Use a lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /fitness_app

# Copy dependency file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all Python source files
# This includes both top-level and nested Python files
COPY fitness_app/*.py fitness_app/
COPY fitness_app/versions/*.py fitness_app/versions/

# copy everything inside the fitness_app folder
# including any future subdirectories, configs, etc.
# COPY fitness_app/ ./fitness_app/

# Set default command to run the main app
CMD ["python", "fitness_app/ACEest_Fitness.py"]