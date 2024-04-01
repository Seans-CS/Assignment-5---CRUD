from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .dependencies import database
from . import models, schemas, sandwiches

app = FastAPI()


# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Endpoint to create a new sandwich
@app.post("/sandwiches/", response_model=schemas.Sandwich)
def create_sandwich(sandwich: schemas.SandwichCreate, db: Session = Depends(get_db)):
    return sandwiches.create(db=db, sandwich=sandwich)


# Endpoint to retrieve all sandwiches
@app.get("/sandwiches/", response_model=list[schemas.Sandwich])
def read_sandwiches(db: Session = Depends(get_db)):
    return sandwiches.read_all(db)


# Endpoint to retrieve a specific sandwich by ID
@app.get("/sandwiches/{sandwich_id}", response_model=schemas.Sandwich)
def read_sandwich(sandwich_id: int, db: Session = Depends(get_db)):
    sandwich = sandwiches.read_one(db=db, sandwich_id=sandwich_id)
    if sandwich is None:
        raise HTTPException(status_code=404, detail="Sandwich not found")
    return sandwich


# Endpoint to update a sandwich by ID
@app.put("/sandwiches/{sandwich_id}", response_model=schemas.Sandwich)
def update_sandwich(sandwich_id: int, sandwich: schemas.SandwichUpdate, db: Session = Depends(get_db)):
    return sandwiches.update(db=db, sandwich_id=sandwich_id, sandwich=sandwich)


# Endpoint to delete a sandwich by ID
@app.delete("/sandwiches/{sandwich_id}")
def delete_sandwich(sandwich_id: int, db: Session = Depends(get_db)):
    return sandwiches.delete(db=db, sandwich_id=sandwich_id)
