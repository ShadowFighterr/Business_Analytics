Assignment 4: Prometheus & Grafana Monitoring Stack

This project sets up a complete monitoring and visualization stack using Prometheus and Grafana, all containerized with Docker Compose. It is built to fulfill the requirements for Assignment 4.

The stack monitors three different data sources:

A PostgreSQL Database (using postgres_exporter)

The Host System's Metrics (using node_exporter)

External API Data (using a custom Python exporter for live weather data)

Components

Prometheus: The monitoring server, collects and stores all metrics.

Grafana: The visualization platform, used to create dashboards from Prometheus data.

PostgreSQL Exporter: A service that scrapes metrics from a PostgreSQL database.

Node Exporter: A service that scrapes system-level metrics from the host machine (CPU, RAM, Disk, etc.).

Custom Python Exporter: A Python script that fetches live weather data for Astana from the Open-Meteo API and exposes it for Prometheus to scrape.

How to Run This Project

Prerequisites

Docker and Docker Compose

Python 3.8+ and pip

A running PostgreSQL database (e.g., classicmodels) that is accessible to Docker.

Step 1: Configuration

Database Connection:
Open the docker-compose.yml file. Find the postgres_exporter service and update the DATA_SOURCE_NAME environment variable with your correct PostgreSQL username, password, host IP, and database name.

environment:
  DATA_SOURCE_NAME: "postgresql://YOUR_USER:YOUR_PASSWORD@YOUR_IP:5432/your_database?sslmode=disable"


(Note: Use your host IP, not localhost, so the container can find it.)

Prometheus Targets:
Open prometheus.yml. The targets are pre-configured to use the Docker service names (e.g., node_exporter:9100) and host.docker.internal:8000 for the custom exporter.

Step 2: Run the Monitoring Stack

In your terminal, run the following command to start all the main services:

docker compose up -d


This will start Prometheus, Grafana, Node Exporter, and the PostgreSQL Exporter.

Step 3: Run the Custom Python Exporter

This script must be run outside of Docker, on your host machine.

Create and activate a virtual environment:

python3 -m venv venv
source venv/bin/activate


Install dependencies:

pip install prometheus_client requests


Run the script:

python custom_exporter.py


You should see Custom exporter started on http://localhost:8000. Leave this terminal running.

Accessing the Services

Prometheus: http://localhost:9090

Go to Status > Targets to verify all services are UP.

Grafana: http://localhost:3000

Login: admin / admin (or as set in your docker-compose.yml)

Importing the Dashboards

The three dashboards are included in this repository as .json files.

In Grafana, go to the Dashboards section on the left.

Click New > Import.

Drag and drop one of the .json files (e.g., dashboard-database.json) into the upload area.

Select your prometheus data source.

Click Import.

Repeat for the other two dashboard files.

Repository Files

docker-compose.yml: Defines all Docker services.

prometheus.yml: Prometheus configuration file with all scrape targets.

custom_exporter.py: Python script to fetch live weather data for Dashboard 3.

dashboard-database.json: Grafana dashboard for PostgreSQL metrics (Dashboard 1).

dashboard-node-exporter.json: Grafana dashboard for system metrics (Dashboard 2).

dashboard-custom-weather.json: Grafana dashboard for live weather data (Dashboard 3).

README.md: This file.
