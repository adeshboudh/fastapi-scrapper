# FastAPI Scraper

This project is a FastAPI application designed for scraping URLs from a CSV file. It utilizes PostgreSQL for data storage, Redis as a message broker, and Celery for handling background tasks.

## Project Structure

```
fastapi-scraper
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── celery_worker.py
│   ├── tasks.py
│   └── config.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd fastapi-scraper
   ```

2. **Build and run the application using Docker Compose:**
   ```
   docker-compose up --build
   ```

3. **Access the FastAPI application:**
   Open your browser and navigate to `http://localhost:8000`.

4. **API Documentation:**
   The interactive API documentation can be found at `http://localhost:8000/docs`.

## Usage

- Place your CSV file containing URLs in the designated directory.
- Use the provided API endpoints to trigger the scraping tasks and manage the data.

## Dependencies

This project requires the following Python packages:

- FastAPI
- SQLAlchemy
- Redis
- Celery

These dependencies are listed in the `requirements.txt` file.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.