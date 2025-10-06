from fastapi import FastAPI, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app import models, database
import datetime

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="FastAPI Todo App")

# DBセッション生成
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ホーム
@app.get("/")
def read_root():
    return {"message": "FastAPI Todo App is working!"}

# Todo 作成
@app.post("/todos")
def create_todo(title: str, description: str = "", due_date: str = None, db: Session = Depends(get_db)):
    import datetime
    due = datetime.datetime.fromisoformat(due_date) if due_date else datetime.datetime.utcnow()
    todo = models.Todo(title=title, description=description, due_date=due)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo

# Todo 一覧取得
@app.get("/todos")
def get_todos(db: Session = Depends(get_db)):
    return db.query(models.Todo).all()

# Todo 更新（完了フラグ）
@app.put("/todos/{todo_id}/toggle")
def toggle_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not todo:
        return {"error": "Todo not found"}
    todo.is_done = not todo.is_done
    db.commit()
    db.refresh(todo)
    return todo

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    db = database.SessionLocal()
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not todo:
        db.close()
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
    db.close()
    return {"message": f"Todo with ID {todo_id} deleted successfully"}

@app.put("/todos/{todo_id}")
def update_todo(
    todo_id: int,
    title: str = Body(None),
    description: str = Body(None),
    due_date: str = Body(None),
):
    db = database.SessionLocal()
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not todo:
        db.close()
        raise HTTPException(status_code=404, detail="Todo not found")

    # 更新処理
    if title is not None:
        todo.title = title
    if description is not None:
        todo.description = description
    if due_date is not None:
        try:
            todo.due_date = datetime.datetime.fromisoformat(due_date)
        except ValueError:
            db.close()
            raise HTTPException(status_code=400, detail="Invalid due_date format. Use YYYY-MM-DD")

    db.commit()
    db.refresh(todo)
    db.close()
    return todo