# Bitcoin Real-Time ETL Pipeline

A complete **ETL (Extract, Transform, Load)** pipeline designed to collect, transform, and store real-time **Bitcoin (BTC)** price data using the public Coinbase API.  
This project demonstrates best practices in **data engineering**, integrating continuous data capture, persistence in a database, and structured data storage.

---

## Overview

This project implements an end-to-end solution for real-time data collection and storage:

- Extract current Bitcoin price directly from the **Coinbase API**.  
- Transform and standardize the raw JSON data into a structured format.  
- Load the processed data into either **PostgreSQL** or **TinyDB** for storage.  

The pipeline is ideal for educational purposes and as a reference for **real-time ETL architecture**.

---

## ETL Flow

The pipeline follows these steps, reflecting the scripts in this repository:

### 1. Extract
- Fetches the current Bitcoin price from Coinbase API: `https://api.coinbase.com/v2/prices/spot`.  
- Returns JSON containing:
  - `amount` (current price)  
  - `base` (cryptocurrency, e.g., BTC)  
  - `currency` (e.g., USD)  

### 2. Transform
- Converts raw JSON into a Python dictionary.  
- Adds a `timestamp` field for when the data was collected.  
- For PostgreSQL: `amount` is converted to `float`.  
- For TinyDB: `amount` is stored as-is.  

### 3. Load
- **PostgreSQL**:
  - Connects using credentials from `.env`.  
  - Inserts into the `bitcoin_data` table:  
    `id SERIAL, value NUMERIC, cryptocurrency VARCHAR, currency VARCHAR, timestamp TIMESTAMP`.  
  - Creates the table if it does not exist.  
- **TinyDB**:
  - Inserts data into a local JSON file (`bitcoin_json.json`) using TinyDB.  
  - Suitable for testing or development environments.  

### 4. Looping / Scheduling
- After loading, the pipeline waits **12 seconds** (`time.sleep(12)`) before fetching the next data point.  
- Continues indefinitely until interrupted by the user (KeyboardInterrupt).

---

## Technologies Used

| Category         | Technology          | Description                                     |
|-----------------|-------------------|-----------------------------------------------|
| Language        | **Python 3**       | Core programming language                     |
| Dependency Management | **Poetry**     | Handles virtual environment and dependencies |
| Data Collection | **Requests**       | Fetches data from the Coinbase API           |
| Database        | **PostgreSQL**     | Relational database storage (optional)       |
| Lightweight DB  | **TinyDB**         | Simple local JSON database (optional)        |
| Database Driver | **psycopg2**       | PostgreSQL Python driver                      |
| Configuration   | **python-dotenv**  | Loads environment variables from `.env` file |

---

## How to Run

1. Clone the repository**
   
Clone the repository and navigate to the project folder:

```bash
git clone https://github.com/joycemsm/etl-pipeline-bitcoin.git
cd etl-pipeline-bitcoin 

2. Install project dependencies:

```bash
poetry install

3. Create a .env file in the root (for PostgreSQL ETL) with your database credentials:

```env
DB_NAME=your_db_name
DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

4. Run the ETL pipeline:

poetry run python src/pipeline01.py


