from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import models, schemas, crud, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Todo App")

# ✅ CORS設定
origins = [
    "http://localhost:5173",  # Vite (React開発用)
    "http://127.0.0.1:5173",  # 一部ブラウザでの別表記
    "http://localhost:3000",  # 将来的にcreate-react-appを使う場合に備えて
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーティング
@app.get("/todos", response_model=list[schemas.Todo])
def read_todos(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    return crud.get_todos(db, skip, limit)

@app.get("/todos/{todo_id}", response_model=schemas.Todo)
def read_todo(todo_id: int, db: Session = Depends(database.get_db)):
    todo = crud.get_todo(db, todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.post("/todos", response_model=schemas.Todo)
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(database.get_db)):
    return crud.create_todo(db, todo)

@app.put("/todos/{todo_id}", response_model=schemas.Todo)
def update_todo(todo_id: int, todo: schemas.TodoUpdate, db: Session = Depends(database.get_db)):
    updated = crud.update_todo(db, todo_id, todo)
    if updated is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return updated

@app.delete("/todos/{todo_id}", response_model=schemas.Todo)
def delete_todo(todo_id: int, db: Session = Depends(database.get_db)):
    deleted = crud.delete_todo(db, todo_id)
    if deleted is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return deleted
