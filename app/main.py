from datetime import timedelta
from fastapi import FastAPI, Depends, UploadFile, File, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from . import models, schemas, crud, config, database, auth
from .tasks import scrape_urls

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(auth.get_current_user)):
    return current_user

@app.post("/upload", response_model=schemas.Task)
def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Invalid file format. Only CSV files are allowed.")
    
    task = crud.create_task(db=db)
    scrape_urls.delay(task.id, file.file.read().decode('utf-8'))
    return task

@app.get("/status/{task_id}", response_model=schemas.Task)
def get_status(task_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    task = crud.get_task_result(db=db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.get("/results/{task_id}")
def get_results(task_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(auth.get_current_user)):

    task = crud.get_task(db=db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task