# controllers/sandwiches.py
from sqlalchemy.orm import Session
from ..models import models
from .. import schemas


def create_sandwich(db: Session, sandwich: schemas.SandwichCreate):
    db_sandwich = models.Sandwich(**sandwich.dict())
    db.add(db_sandwich)
    db.commit()
    db.refresh(db_sandwich)
    return db_sandwich


def get_all_sandwiches(db: Session):
    return db.query(models.Sandwich).all()


def get_sandwich_by_id(db: Session, sandwich_id: int):
    return db.query(models.Sandwich).filter(models.Sandwich.id == sandwich_id).first()


def update_sandwich(db: Session, sandwich_id: int, sandwich: schemas.SandwichUpdate):
    db_sandwich = db.query(models.Sandwich).filter(models.Sandwich.id == sandwich_id).first()
    if db_sandwich:
        for key, value in sandwich.dict(exclude_unset=True).items():
            setattr(db_sandwich, key, value)
        db.commit()
        db.refresh(db_sandwich)
    return db_sandwich


def delete_sandwich(db: Session, sandwich_id: int):
    db_sandwich = db.query(models.Sandwich).filter(models.Sandwich.id == sandwich_id).first()
    if db_sandwich:
        db.delete(db_sandwich)
        db.commit()
    return None
