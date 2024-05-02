from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated, List
import models as models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import auth
from auth import get_current_user

from fastapi.middleware.cors import CORSMiddleware

# uvicorn main:app --reload
# api on port 8000
# React app on port 3000
TOTAL_AMMO_TYPES = 160
app = FastAPI()
app.include_router(auth.router)

# a different application is allowed to call our fastapi application iff it is running on our local host on port 3000

origins = [
    "http://localhost:3000",
]
# add origins to application
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

# pydantic models validate requests from React application
# use pydantic validators
class EntryBase(BaseModel): # updating user number of each ammo
    ammo_name: str
    caliber: str
    ammo_amount: int
    user_id: int
    
class LookupBase(BaseModel): # lookup info of ammo from static database
    ammo_name: str
    caliber: str
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
user_dependency = Annotated[dict, Depends(get_current_user)]

models.Base.metadata.create_all(bind=engine)

# validate the user's ammo and caliber with the tarkov_ammo datatable
def validate_ammo(db, name, caliber) -> bool: 
    try:
        validate_ammo = db.query(models.TarkovAmmo).filter(
            models.TarkovAmmo.ammo_name == name and
            models.TarkovAmmo.caliber == caliber
        ).first()
        if not validate_ammo:
            return False
        else:
            return True
    finally:
        db.close()

# get current user information
@app.get("/", status_code=status.HTTP_200_OK)
async def user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return {"User": user}

# GET static ammo database
@app.get("/tarkov_ammo/{ammo_name}/{caliber}}", status_code=status.HTTP_200_OK)
async def read_ammo(ammo_name: str, caliber: str, db: db_dependency) -> (LookupBase | None): # data inputted needs to have underscores
    ammo = db.query(models.TarkovAmmo).filter(
            models.TarkovAmmo.ammo_name == ammo_name and
            models.TarkovAmmo.caliber == caliber
        ).first()
    if ammo is None:
        raise HTTPException(status_code=404, detail='Ammo and caliber not found')
    return ammo

# CREATE ammo entry
@app.post("/entries/", status_code=status.HTTP_201_CREATED)
async def create_entry(entry: EntryBase, db: db_dependency) -> None:
    db_entry = models.Entry(**entry.model_dump())
    if not validate_ammo(db, entry.ammo_name, entry.caliber): # use pydantic validation
        # prompt user again 
        raise HTTPException(status_code=404, detail='Invalid Entry')
    db.add(db_entry)
    db.commit()

# GET entries at user_id
@app.get("/entries/{user_id}", status_code=status.HTTP_200_OK)
async def read_entries(user_id: int, db: db_dependency, skip: int = 0, limit: int = TOTAL_AMMO_TYPES): # compare with user id
    entry = db.query(models.Entry).filter(models.Entry.user_id == user_id).offset(skip).limit(limit).all()
    if entry is None:
        raise HTTPException(status_code=404, detail='Entries were not found')
    return entry

# GET user data
@app.get("/users/", status_code=status.HTTP_200_OK)
async def read_user(user_id: int, db: db_dependency) -> (UserBase | None):
    user = db.query(models.User).filter(models.User.id == user_id).all()
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return user 

# DELETE user AND their entries
@app.delete('/users/{user_id}', status_code=status.HTTP_200_OK)
async def delete_user(user_id: int, db: db_dependency) -> None:
    db_user_entry = db.query(models.Entry).filter(models.Entry.user_id == user_id).all()
    if db_user_entry:
        for entry in db_user_entry:
            db.delete(entry) # delete entry at user_id if it exists
    db_user = db.query(models.User).filter(models.User.id == user_id).first() # delete user at id
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    db.delete(db_user)
    db.commit()
