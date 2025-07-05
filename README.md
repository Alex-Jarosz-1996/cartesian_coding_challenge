# Cartesian Coding Challenge
## Overview
This is a Python-based web service that provides electricity price information based on historical data.  
The application:

- Fetches half-hourly electricity price data from a public github CSV URL.
- Stores the data in a PostgreSQL database.
- Allows users to query the **mean price** for a specific state.

The service runs on `http://localhost:8000`.

## API Endpoints
This project utilises the following API endpoints:

### 1. `GET /api/electricity/get_data`
Fetches the electricity price CSV from the configured URL and populates the database.

#### Response Codes:
- `201 Created`: Electricity data saved into the database.
- `200 OK`: Data already exists, no action taken.
- `404 Not Found`: No electricity data found at the source.
- `500 Internal Server Error`: Unexpected error.

### 2. `DELETE /api/electricity/delete_data`
Deletes all electricity price data from the database.

#### Response Codes:
- `200 OK`: Deleted existing electricity data.
- `200 OK`: No data to delete.
- `500 Internal Server Error`: Unexpected error.

### 3. `GET /api/electricity/get_mean/<state>`
Returns the mean electricity price for the given state.

#### HTTP response codes:
- `201 Created`:  Mean price returned.
- `404 Not Found`: No data for the requested state.
- `500 Internal Server Error`: Unexpected error.

## Quickstart
1. Clone the repo
```bash
git clone <repo>
cd cartesian_coding_challenge
```
2. Create a .env file at project root with the key/value pairs specified below.
3. Build and run the app with Docker
```bash
docker-compose build
docker-compose up
```

## Example usage workflow
Once the docker is running, and using postman / curl:
### 1. Trigger data load
```
GET /api/electricity/get_data
```
### 2. Query the mean price for a state:
```
GET /api/electricity/get_mean/VIC
```
### 3. Delete electricity data (optional)
```
DELETE /api/electricity/delete_data
```

## Environment Variables
Configured in e `.env` file:
```
SECRET_KEY='django-secret-key'
GITHUB_CSV_URL='github-csv-url'

DEBUG=True

DB_NAME=xxx
DB_USER=xxx
DB_PASSWORD=xxx
DB_HOST=db
DB_PORT=5432
```

## Test harness execution
Unit test can be executed with the following command:
```python
cd cartesian
python3 manage.py test
```

