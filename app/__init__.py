# FILE: /fastapi-scraper/fastapi-scraper/app/__init__.py
from fastapi import FastAPI

app = FastAPI()

from . import models, schemas, crud, tasks

# Initialize the database and other components here if needed.