from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from contextlib import contextmanager
import models, schemas
from database import SessionLocal

app = FastAPI()

@contextmanager
def with_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_db_todo_item(db: Session, todo_id: int):
    return db.query(models.TodoItem).filter(models.TodoItem.id == todo_id).first()

@app.post("/todo/", response_model=schemas.TodoItem)
def create_todo_item(todo_item: schemas.TodoItemCreate, db: Session = Depends(with_db_session)):
    db_todo_item = models.TodoItem(**todo_item.dict())
    db.add(db_todo_item)
    db.commit()
    db.refresh(db_todo_item)
    return db_todo_item

@app.put("/todo/{todo_id}", response_model=schemas.TodoItem)
def update_todo_item(todo_id: int, todo_item: schemas.TodoItemBase, db: Session = Depends(with_db_session)):
    db_todo_item = get_db_todo_item(db, todo_id)
    if db_todo_item is None:
        raise HTTPException(status_code=404, detail="TodoItem not found")
    for attr in todo_item.dict().keys():
        setattr(db_todo_item, attr, getattr(todo_item, attr))
    db.commit()
    db.refresh(db_todo_item)
    return db_todo_item

@app.get("/todo/", response_model=list[schemas.TodoItem])
def read_todo_items(skip: int = 0, limit: int = 100, db: Session = Depends(with_db_session)):
    return db.query(models.TodoItem).offset(skip).limit(limit).all()

@app.get("/todo/{todo_id}", response_model=schemas.TodoItem)
def read_todo_item(todo_id: int, db: Session = Depends(with_db_session)):
    db_todo_item = get_db_todo_item(db, todo_id)
    if db_todo_item is None:
        raise HTTPException(status_code=404, detail="TodoItem not found")
    return db_todo_item

@app.delete("/todo/{todo_id}", status_code=204)
def delete_todo_item(todo_id: int, db: Session = Depends(with_db_session)):
    db_todo_item = get_db_todo_item(db, todo_id)
    if db_todo_item is None:
        raise HTTPException(status_code=404, detail="TodoItem not found")
    db.delete(db_todo_item)
    db.commit()
    return {"status": "TodoItem deleted"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)