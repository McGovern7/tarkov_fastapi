from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated, List
import models as models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware

# uvicorn main:app --reload
# api on port 8000
# React app on port 3000
TOTAL_AMMO_TYPES = 160
app = FastAPI()

# a different application is allowed to call our faspapi application iff it is running on our local host on port 3000
origins = [
    'http://localhost:3000'
]
# add origins to application
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
)

# pydantic models validate requests from React application
class EntryBase(BaseModel): # updating user number of each ammo
    ammo_name: str
    calibre: str
    ammo_amount: int
    user_id: int

class EntryModel(EntryBase):
    id: int

    class Config:
        orm_mode = True
    
class LookupBase(BaseModel): # lookup info of ammo from static database
    ammo_name: str
    calibre: str
    penetration: int
    damage: int
    velocity: int
    frag_pct: int

class UserBase(BaseModel): # username and ID
    username: str

def get_db(): # dont have db open too long
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

models.Base.metadata.create_all(bind=engine)

def validate_ammo(db, name, calibre) -> bool: # validate the user's ammo and calibre with the tarkov_ammo datatable
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

# GET static ammo database
@app.get("/tarkov_ammo/{ammo_name}/{calibre}}", status_code=status.HTTP_200_OK)
async def read_ammo(ammo_name: str, calibre: str, db: db_dependency) -> (LookupBase | None): # data inputted needs to have underscores
    ammo = db.query(models.TarkovAmmo).filter(
            models.TarkovAmmo.ammo_name == ammo_name and
            models.TarkovAmmo.calibre == calibre
        ).first()
    if ammo is None:
        raise HTTPException(status_code=404, detail='Ammo and calibre not found')
    print(ammo)
    return ammo

# CREATE ammo entry
@app.post("/entries/", response_model=EntryModel, status_code=status.HTTP_201_CREATED)
async def create_entry(entry: EntryBase, db: db_dependency) -> None:
    db_entry = models.Entry(**entry.model_dump())
    if not validate_ammo(db, entry.ammo_name, entry.calibre): # validate for matching [ammo_name, calibre] row in
        # prompt user again 
        raise HTTPException(status_code=404, detail='Invalid Entry')
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

# GET user's entries
@app.get("/entries/{user_id}", response_model=List[EntryModel], status_code=status.HTTP_200_OK)
async def read_entries(user_id: int, db: db_dependency, skip: int = 0, limit: int = TOTAL_AMMO_TYPES): # compare with user id
    entry = db.query(models.Entry).filter(models.Entry.user_id == user_id).offset(skip).limit(limit).all()
    if entry is None:
        raise HTTPException(status_code=404, detail='Entries were not found')
    return entry

# CREATE and save a user
@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: db_dependency):
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()

# GET user data
@app.get("/users/{user_id}", status_code=status.HTTP_200_OK)
async def read_user(user_id: int, db: db_dependency) -> (UserBase | None):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return user 

# DELETE user and their entries
@app.delete('/users/{username}', status_code=status.HTTP_200_OK)
async def delete_user(user_id: int, db: db_dependency) -> None:
    db_user = db.query(models.User).filter(models.User.id == user_id).first() # delete user at id
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    db.delete(db_user)
    db_user_entry = db.query(models.Entry).filter(models.Entry.user_id == user_id).first()
    if db_user_entry:
        db.delete(db_user_entry) # delete entry at user_id if it exists

    db.commit()

# stor
# Create and put into user ammo db are different?
