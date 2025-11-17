# FastAPI Weather Service  
A fully asynchronous **FastAPI-based Weather API**, featuring caching, local JSON storage, SQLite logging, Docker support, testing, and a clean cloud-ready architecture.

---

## Features

### API Endpoint  
- `GET /weather?city=CityName`
- Fetches weather data from **OpenWeatherMap** (fallback to Open-Meteo if no API key)
- Graceful error handling for invalid city/API issues

### Fully Asynchronous  
- Built using `asyncio` + `httpx.AsyncClient`
- High performance and non-blocking

### Local Storage  
- Saves weather responses as JSON files  
- Stored inside `data/`  
- Filename format:  


###  SQLite Logging  
Every request is logged with:

| Field | Description |
|-------|-------------|
| `city` | The requested city |
| `timestamp` | UTC time of the request |
| `file_path` | Location of saved JSON file |

### Caching  
- 5-minute cache TTL  
- Returns cached responses instantly  
- Reduces API usage and improves speed

###  Rate Limiting  
- In-memory limiter  
- Default: **30 requests/minute per IP**

###  Docker Support  
- `Dockerfile` and `docker-compose.yml` included  
- Runs in a clean, isolated environment

###  Tests Included  
- Written using `pytest` + `pytest-asyncio`

---

---

##  Installation (Local)

### Clone the repository

```bash
git clone https://github.com/your-username/fastapi-weather.git
cd fastapi-weather

### Create the virtual env
python -m venv venv
venv\Scripts\activate

### Install requirements
pip install -r requirements.txt

### Create .env file
Copy the .env.example file

### Run the api
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Running with Docker
### Build the Docker image
docker compose build

### Run the container
docker compose up
