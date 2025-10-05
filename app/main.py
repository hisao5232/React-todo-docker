from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app import models, database

# database から必要なものをインポート
from app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI + PostgreSQL Example")

# DBセッションを生成・破棄する関数
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "FastAPI + PostgreSQL + Docker is working!"}

@app.post("/users")
def create_user(name: str, email: str, db: Session = Depends(get_db)):
    user = models.User(name=name, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()
