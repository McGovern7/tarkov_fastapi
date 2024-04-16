from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class UpdateAmmoBase(BaseModel):
    ammo_name: str
    calibre: str
    ammo_amount: int
    user_id: int

class AmmoBase(BaseModel):
    ammo_name: str
    calibre: str
    penetration: int
    damage: int
    velocity: int
    frag_pct: int

class UserBase(BaseModel):
    username: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

def validate_ammo(db, name, calibre): # validate the user's ammo and calibre
    db = SessionLocal()
    try:
        validate_ammo = db.query(models.TarkovAmmo).filter(
            models.TarkovAmmo.ammo_name == name and
            models.TarkovAmmo.calibre == calibre
        ).first()
        print(validate_ammo)
        if not validate_ammo:
            print("check false")
            return False
        else:
            print("check true")
            return True
    finally:
        db.close()

@app.post("/")

@app.post("/updates/", status_code=status.HTTP_201_CREATED)
async def create_update(update: UpdateAmmoBase, db: db_dependency):
    db_update = models.UpdateAmmo(**update.model_dump())
    if not validate_ammo(db, update.ammo_name, update.calibre): # validate for matching [ammo_name, calibre] row in 
        HTTPException(status_code=404, detail='Invalid Ammo Name or Calibre')
    db.add(db_update)
    db.commit()    

@app.get("/updates/{user_id}", status_code=status.HTTP_200_OK)
async def read_update(user_id: int, db: db_dependency): # compare with user id
    update = db.query(models.UpdateAmmo).filter(models.UpdateAmmo.id == user_id).first()
    if update is None:
        HTTPException(status_code=404, detail='Post was not found')
    return update

# api endpoint, create and save a user
@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: db_dependency):
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()

@app.get("/users/{user_id}", status_code=status.HTTP_200_OK)
async def read_user(user_id: int, db: db_dependency):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return user 