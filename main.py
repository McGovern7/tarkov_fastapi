from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated, List
import models as models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import auth
# from auth import verify_user_token
from fastapi.middleware.cors import CORSMiddleware

# uvicorn main:app --reload
# api on port 8000
# React app on port 3000
TOTAL_AMMO_TYPES = 160
app = FastAPI()
app.include_router(auth.router)

# a different application is allowed to call our fastapi application iff it is running on our local host on port 3000

origins = [
    "http://localhost:3000", # adjust port if running on different server
]
# add origins to application
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # allow all origins from the list
    allow_credentials=True,
    allow_methods=['*'], # allow all methods
    allow_headers=['*'] # allow all headers
)

# pydantic models validate requests from React application
# use pydantic validators
class EntryBase(BaseModel): # updating user number of each ammo
    ammo_name: str
    caliber: str
    ammo_amount: int
    username: str
    
class LookupBase(BaseModel): # lookup info of ammo from static database
    ammo_name: str
    caliber: str
    penetration: int
    damage: int
    velocity: int
    frag_pct: int
    ammo_group: int

class UserBase(BaseModel): # username and ID
    username: str

def get_db(): # dont have db open too long
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
# user_dependency = Annotated[dict, Depends(verify_user_token)]

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
'''
def findDuplicate(db, entry) -> int:
    try:
        findDuplicate = db.query(models.Entry).filter(
            models.Entry.ammo_name == entry.ammo_name and
            models.Entry.caliber == entry.caliber and
            models.Entry.username == entry.username
        ).first()
        if not findDuplicate:
            return -1
        else:
            return models.Entry.id
    finally:
        db.close()
'''
# Get all ammo info ordered by caliber, then armor penetration, then damage
@app.get("/tarkov_ammo/", status_code=status.HTTP_200_OK)
async def read_all_ammo(db: db_dependency, limit: int = TOTAL_AMMO_TYPES):
    type = db.query(models.TarkovAmmo).order_by(
        models.TarkovAmmo.ammo_group.asc(),
        models.TarkovAmmo.penetration.asc(),
        models.TarkovAmmo.damage.asc(),
    ).limit(limit).all()
    if type is None:
        raise HTTPException(status_code=404, detail='Ammo Table not found')
    return type

    
# GET static ammo from ammo database
@app.get("/tarkov_ammo/{ammo_group}/{ammo_name}", status_code=status.HTTP_200_OK)
async def read_ammo(ammo_name: str, caliber: str, db: db_dependency) -> (UserBase | None): # data inputted needs to have underscores
    ammo = db.query(models.TarkovAmmo).filter(
            models.TarkovAmmo.ammo_name == ammo_name and
            models.TarkovAmmo.caliber == caliber
        ).first()
    if ammo is None:
        raise HTTPException(status_code=404, detail='Ammo and caliber not found')
    return ammo
    

# CREATE ammo entry
# TODO: repeat entries combine numbers
@app.post("/entries/", status_code=status.HTTP_201_CREATED)
async def create_entry(entry: EntryBase, db: db_dependency) -> None:
    db_entry = models.Entry(**entry.model_dump())
    if not validate_ammo(db, entry.ammo_name, entry.caliber): # use pydantic validation
        # prompt user again 
        raise HTTPException(status_code=404, detail='Invalid Entry')
    #dupe_id = findDuplicate(db, entry)
    #if dupe_id >= 0:
    #    patch_duplicate(entry, dupe_id, db) # append onto existing
    #else:
    db.add(db_entry)
    db.commit()

#@app.patch("/entries/", status_code=status.HTTP_201_CREATED)
#async def patch_duplicate(entry: EntryBase, dupe_id: int, db: db_dependency) -> None:


# GET entries at username
@app.get("/entries/{username}", status_code=status.HTTP_200_OK)
async def read_entries(username: str, db: db_dependency, skip: int = 0, limit: int = TOTAL_AMMO_TYPES): # compare with user id
    entry = db.query(models.Entry).filter(models.Entry.username == username).offset(skip).limit(limit).all()
    if entry is None:
        raise HTTPException(status_code=404, detail='Entries were not found')
    return entry


# DELETE user AND their entries
@app.delete('/users/{username}', status_code=status.HTTP_200_OK)
async def delete_user(username: str, db: db_dependency) -> None:
    db_user_entry = db.query(models.Entry).filter(models.Entry.username == username).all()
    if db_user_entry: 
        for entry in db_user_entry: # len(entries) runtime
            db.delete(entry) # delete entry at user_id if it exists
    db_user = db.query(models.User).filter(models.User.username == username).first() # delete user at id
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    db.delete(db_user)
    db.commit()
