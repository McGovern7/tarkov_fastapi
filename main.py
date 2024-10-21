from fastapi import FastAPI, Body, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Annotated, List, Optional
import models as models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import auth
# from auth import verify_user_token

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

class DupeBase(BaseModel):
    id: int
    ammo_amount: int

class PatchData(BaseModel):
    newAmount: int

class LookupBase(BaseModel): # lookup info of ammo from static database
    ammo_name: str
    caliber: str
    penetration: Optional[int]
    damage: Optional[int]
    velocity: Optional[int]
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

# Get all ammo info ordered by caliber, then armor penetration, then damage
@app.get("/tarkov_ammo/", status_code=status.HTTP_200_OK)
async def read_all_ammo(db: db_dependency, limit: int = TOTAL_AMMO_TYPES) -> List[LookupBase]:
    type = db.query(models.TarkovAmmo).order_by(
        models.TarkovAmmo.ammo_group.asc(),
        models.TarkovAmmo.penetration.asc(),
        models.TarkovAmmo.damage.asc(),
    ).limit(limit).all()
    if type is None:
        raise HTTPException(status_code=404, detail='Ammo table not found')
    return type

    
# GET static ammo from ammo database
@app.get("/tarkov_ammo/{caliber}/{ammo_name}", status_code=status.HTTP_200_OK)
async def read_ammo(ammo_name: str, caliber: str, db: db_dependency) -> bool: # data inputted needs to have underscores
    ammo = db.query(models.TarkovAmmo).filter(
            models.TarkovAmmo.ammo_name == ammo_name,
            models.TarkovAmmo.caliber == caliber,
        ).first()
    if ammo is None:
        raise HTTPException(status_code=404, detail='Ammo matching input not found')
    return True
    

# CREATE ammo entry
@app.post("/entries/", status_code=status.HTTP_201_CREATED)
async def create_entry(entry: EntryBase, db: db_dependency) -> None:
    db_entry = models.Entry(**entry.model_dump())
    if not validate_ammo(db, entry.ammo_name, entry.caliber): # use pydantic validation
        # prompt user again 
        raise HTTPException(status_code=404, detail='Invalid Entry')
    db.add(db_entry)
    db.commit()

# GET message needed to find the old entry being duplicated, required for the PATCH call
@app.get("/entries/{username}/{caliber}/{ammo_name}", status_code=status.HTTP_200_OK)
async def get_duplicate(username: str, caliber: str, ammo_name: str, db: db_dependency) -> DupeBase:
    # get specific id
    duplicate = db.query(models.Entry).filter(
        models.Entry.username == username,
        models.Entry.caliber == caliber,
        models.Entry.ammo_name == ammo_name,
        ).first()
    if duplicate is None:
        raise HTTPException(status_code=404, detail='No duplicate entry')
    return duplicate

# PATCH existing entry with new ammount
@app.patch("/entries/{id}")
async def patch_duplicate(id: int, data: PatchData, db: db_dependency) -> None:
    patched_entry = db.query(models.Entry).filter(models.Entry.id == id).first()
    if not patched_entry:
        raise HTTPException(status_code=404, detail='Entry with that ID not found')
    # patch the fields
    patched_entry.ammo_amount = data.newAmount
    db.add(patched_entry)
    db.commit()

# GET entries at username
@app.get("/entries/{username}", status_code=status.HTTP_200_OK)
async def read_entries(username: str, db: db_dependency, skip: int = 0, limit: int = TOTAL_AMMO_TYPES) -> (List[EntryBase] | None):
    entry = db.query(models.Entry).filter(models.Entry.username == username).offset(skip).limit(limit).all()
    if len(entry) == 0:
        raise HTTPException(status_code=404, detail='No Entries Associated with {}'.format(username))
    return entry

# DELETE user's entries
@app.delete("/entries/{username}", status_code=status.HTTP_200_OK)
async def delete_user(username: str, db: db_dependency) -> None:
    db_user_entry = await read_entries(username=username, db=db) # O(nm) n = totalEntries m = filteredEntries
    if db_user_entry: 
        for entry in db_user_entry: # len(entries) runtime
            db.delete(entry) # delete entry at user_id if it exists
    db.commit()
    

# DELETE user 
@app.delete('/users/{username}', status_code=status.HTTP_200_OK)
async def delete_user(username: str, db: db_dependency) -> None:
    db_user = db.query(models.User).filter(models.User.username == username).first() # delete user at id
    if not db_user:
        raise HTTPException(status_code=404, detail='User not found')
    db.delete(db_user)
    db.commit()
