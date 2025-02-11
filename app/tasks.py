from celery import shared_task
from . import crud, models, schemas
from .database import SessionLocal
import requests
from bs4 import BeautifulSoup
import random

@shared_task
def scrape_urls(task_id: int, csv_content: str):
    db = SessionLocal()
    try:
        urls = csv_content.splitlines()
        print(urls)
        for url in urls:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            title = soup.title.string if soup.title else None
            description = soup.find('meta', attrs={'name': 'description'})
            description = description['content'] if description else None
            keywords = soup.find('meta', attrs={'name': 'keywords'})
            keywords = keywords['content'] if keywords else None

            result = schemas.TaskResult(
                url=url,
                title=title,
                description=description,
                keywords=keywords,
                id=random.randint(1, 100)
            )
            print(result)
            crud.create_task_result(db=db, task_id=task_id, result=result)
        
        task = crud.get_task(db=db, task_id=task_id)
        task.status = "completed"
        db.commit()
    except Exception as e:
        task = crud.get_task(db=db, task_id=task_id)
        print(e)
        task.status = "failed"
        db.commit()
    finally:
        db.close()