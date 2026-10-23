# Use an official lightweight Python image
FROM python:3.12-slim

# Set working directory inside the container
WORKDIR /nearfield

# Prevent Python from writing .pyc files and buffer outputs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=tcDigitalCards.settings.production
# Include both the root and the inner directory in Python's lookup path
ENV PYTHONPATH=/nearfield:/nearfield/tcDigitalCards


# Copy requirements and install dependencies
COPY requirements.txt /nearfield/
RUN pip install --no-cache-dir -r requirements.txt && pip install gunicorn

# Copy the rest of your application code
COPY . /nearfield/

# Expose port 8000 for your application
EXPOSE 8000

#Run Gunicorn automatically when the container starts
# REPLACE 'myproject' with the folder name containing your wsgi.py file
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "tcDigitalCards.wsgi:application"]
	
