# 🚀 Assignment 4: Prometheus & Grafana Monitoring Stack

This project sets up a **complete monitoring and visualization stack** using **Prometheus** and **Grafana**, fully containerized with **Docker Compose**.
It fulfills the requirements for **Assignment 4** by monitoring multiple data sources in real time.

---

## 📊 Overview

The stack monitors **three distinct data sources**:

1. 🐘 **PostgreSQL Database** – monitored using **Postgres Exporter**
2. 💻 **Host System Metrics** – collected via **Node Exporter**
3. 🌦️ **External API Data (Weather)** – gathered from **Open-Meteo API** using a **custom Python exporter**

---

## ⚙️ Components

| Component                  | Description                                                                                  |
| -------------------------- | -------------------------------------------------------------------------------------------- |
| **Prometheus**             | Core monitoring server that collects and stores metrics data                                 |
| **Grafana**                | Visualization platform used to create and manage dashboards                                  |
| **PostgreSQL Exporter**    | Scrapes metrics from your PostgreSQL database                                                |
| **Node Exporter**          | Collects system-level metrics (CPU, RAM, Disk, etc.)                                         |
| **Custom Python Exporter** | Fetches live weather data for *Astana* from the Open-Meteo API and exposes it for Prometheus |

---

## 🧰 Prerequisites

Before starting, ensure you have:

* 🐳 **Docker** and **Docker Compose**
* 🐍 **Python 3.8+** and **pip**
* 💾 A running **PostgreSQL database** (e.g., `classicmodels`) accessible from Docker

---

## 🪛 Step 1: Configuration

### 🧩 Database Connection

Open `docker-compose.yml` and update the **PostgreSQL Exporter** service environment variable:

```yaml
environment:
  DATA_SOURCE_NAME: "postgresql://YOUR_USER:YOUR_PASSWORD@YOUR_IP:5432/your_database?sslmode=disable"
```

> ⚠️ **Important:** Use your **host machine IP**, *not* `localhost`, so Docker containers can reach it.

---

### 📡 Prometheus Targets

Check `prometheus.yml` — it comes pre-configured with:

* `node_exporter:9100` (System metrics)
* `postgres_exporter:9187` (Database metrics)
* `host.docker.internal:8000` (Custom Python exporter)

---

## 🏃‍♂️ Step 2: Run the Monitoring Stack

Launch all main services with:

```bash
docker compose up -d
```

This will start:

* Prometheus
* Grafana
* Node Exporter
* PostgreSQL Exporter

---

## 🐍 Step 3: Run the Custom Python Exporter

This exporter runs **outside Docker**, directly on your host machine.

### Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install dependencies:

```bash
pip install prometheus_client requests
```

### Run the exporter:

```bash
python custom_exporter.py
```

✅ You should see:

```
Custom exporter started on http://localhost:8000
```

Keep this terminal open and running.

---

## 🌐 Accessing the Services

| Service        | URL                                            | Description                                                               |
| -------------- | ---------------------------------------------- | ------------------------------------------------------------------------- |
| **Prometheus** | [http://localhost:9090](http://localhost:9090) | Check `Status > Targets` to verify all exporters are *UP*                 |
| **Grafana**    | [http://localhost:3000](http://localhost:3000) | Default login → **admin / admin** (or credentials from your compose file) |

---

## 📈 Importing Dashboards

Three Grafana dashboards are included:

| File                            | Dashboard          |
| ------------------------------- | ------------------ |
| `dashboard-database.json`       | PostgreSQL metrics |
| `dashboard-node-exporter.json`  | System metrics     |
| `dashboard-custom-weather.json` | Live weather data  |

### To import:

1. Open Grafana → **Dashboards** → **New → Import**
2. Drag & drop a `.json` dashboard file
3. Select your **Prometheus** data source
4. Click **Import**
5. Repeat for all three dashboards

---

## 🗂️ Repository Structure

```
📁 assignment4/
├── docker-compose.yml              # Docker service definitions
├── prometheus.yml                  # Prometheus scrape configuration
├── custom_exporter.py              # Custom weather data exporter
├── dashboard-database.json         # Grafana dashboard (PostgreSQL)
├── dashboard-node-exporter.json    # Grafana dashboard (System)
├── dashboard-custom-weather.json   # Grafana dashboard (Weather)
└── README.md                       # This file 😄
```

---

## 🌟 Final Notes

Once everything is up:

* Prometheus continuously scrapes data from all sources
* Grafana visualizes it beautifully across your dashboards
* You can monitor system performance, database activity, and live Astana weather — all in real time 🌤️
