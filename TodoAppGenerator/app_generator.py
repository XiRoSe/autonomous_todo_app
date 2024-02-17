import os

# Define the structure of our project
project_structure = {
    "todo_app": {
    "app": {
        "__init__.py": "# This file can be left empty. It indicates that the app directory is a Python package.",
        "database.py": """
        from sqlalchemy import create_engine
        from sqlalchemy.ext.declarative import declarative_base
        from sqlalchemy.orm import sessionmaker
        
        SQLALCHEMY_DATABASE_URL = "sqlite:///./todo.db"
        engine = create_engine(
            SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
        )
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
        Base = declarative_base()
        """,
        "models.py": """
        from sqlalchemy import Column, Integer, String, Boolean
        from database import Base
        
        class TodoItem(Base):
            __tablename__ = "todo_items"
        
            id = Column(Integer, primary_key=True, index=True)
            title = Column(String, index=True)
            completed = Column(Boolean, default=False)""",
                    "schemas.py": """from pydantic import BaseModel
        
        class TodoItemBase(BaseModel):
            title: str
            completed: bool = False
    
        class TodoItemCreate(TodoItemBase):
            pass
        
        class TodoItem(TodoItemBase):
            id: int
        
            class Config:
                orm_mode = True
        """,
        "main.py": """
        from fastapi import FastAPI, HTTPException, Depends
        from sqlalchemy.orm import Session
        import models, schemas
        from database import SessionLocal, engine
        
        models.Base.metadata.create_all(bind=engine)
        
        app = FastAPI()
        
        # Dependency
        def get_db():
            db = SessionLocal()
            try:
                yield db
            finally:
                db.close()
    
        @app.post("/todo/", response_model=schemas.TodoItem)
        def create_todo_item(todo_item: schemas.TodoItemCreate, db: Session = Depends(get_db)):
            db_todo_item = models.TodoItem(**todo_item.dict())
            db.add(db_todo_item)
            db.commit()
            db.refresh(db_todo_item)
            return db_todo_item
        
        @app.get("/todo/", response_model=list[schemas.TodoItem])
        def read_todo_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
            items = db.query(models.TodoItem).offset(skip).limit(limit).all()
            return items
        
        @app.get("/todo/{todo_id}", response_model=schemas.TodoItem)
        def read_todo_item(todo_id: int, db: Session = Depends(get_db)):
            db_todo_item = db.query(models.TodoItem).filter(models.TodoItem.id == todo_id).first()
            if db_todo_item is None:
                raise HTTPException(status_code=404, detail="TodoItem not found")
            return db_todo_item
    
        @app.put("/todo/{todo_id}", response_model=schemas.TodoItem)
        def update_todo_item(todo_id: int, todo_item: schemas.TodoItemCreate, db: Session = Depends(get_db)):
            db_todo_item = db.query(models.TodoItem).filter(models.TodoItem.id == todo_id).first()
            if db_todo_item is None:
                raise HTTPException(status_code=404, detail="TodoItem not found")
            db_todo_item.title = todo_item.title
            db_todo_item.completed = todo_item.completed
            db.commit()
            db.refresh(db_todo_item)
            return db_todo_item
    
        @app.delete("/todo/{todo_id}", status_code=204)
        def delete_todo_item(todo_id: int, db: Session = Depends(get_db)):
            db_todo_item = db.query(models.TodoItem).filter(models.TodoItem.id == todo_id).first()
            if db_todo_item is not None:
                db.delete(db_todo_item)
                db.commit()
            return {"ok": True}
        """
        },
        "requirements.txt": """
            fastapi==0.75.0
            uvicorn==0.17.6
            sqlalchemy==1.4.27
        """,
        "README.md": """
            # ToDo Application
        
            ## Overview
            This is a simple ToDo application with a FastAPI backend and a SQLite database.
            
            ## Requirements
            - Python 3.8+
            - FastAPI
            - Uvicorn
            - SQLAlchemy
        
            ## Installation
            Install the required packages using pip:
            
            ```bash
            pip install -r requirements.txt
            Running the Application
            Start the application with Uvicorn:
        
            bash
            Copy code
            uvicorn app.main:app --reload
            API Endpoints
            Create a new ToDo item: POST /todo/
            Get all ToDo items: GET /todo/
            Get a single ToDo item by ID: GET /todo/{todo_id}
            Update a ToDo item by ID: PUT /todo/{todo_id}
            Delete a ToDo item by ID: DELETE /todo/{todo_id}
        """
    }
}

def create_project_structure(base_path, structure):
    for name, value in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(value, dict): # It's a directory
            os.makedirs(path, exist_ok=True)
            create_project_structure(path, value)
        else: # It's a file
            with open(path, 'w') as file:
                file.write(value)

if __name__ == "__main__":
    create_project_structure('.', project_structure)
    print("ToDo application structure has been generated successfully.")