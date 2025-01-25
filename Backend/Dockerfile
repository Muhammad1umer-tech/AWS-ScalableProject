# Use the official Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev gcc && \
    apt-get clean

# Copy the requirements file and install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the port for the Chainlit app (default is 8000)
EXPOSE 8000

# Set the default command
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]