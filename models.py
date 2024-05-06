from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from database import Base
# Create Table for MySQL databse

class User(Base):
    __tablename__ = "users"
    # composite key ammo_name, caliber
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(15), unique=True)
    hashed_password = Column(String(64))

class TarkovAmmo(Base):
    __tablename__ = "tarkov_ammo"

    ammo_name = Column(String(25), primary_key=True)
    caliber = Column(String(25), primary_key=True)
    penetration = Column(Integer)
    damage = Column(Integer)
    velocity = Column(Integer)
    frag_pct = Column(Integer)

class Entry(Base): # Ammo Entry
    __tablename__ = 'entries'

    id = Column(Integer, primary_key=True, index=True)
    ammo_name = Column(String(25))
    caliber = Column(String(25))
    ammo_amount = Column(Integer)
    username = Column(String(15), ForeignKey("users.username"))

# storage model has a list of 