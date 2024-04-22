from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from database import Base
# Create Table for MySQL databse

class User(Base):
    __tablename__ = "users"
    # composite key ammo_name, calibre
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(25), unique=True)

class TarkovAmmo(Base):
    __tablename__ = "tarkov_ammo"

    ammo_name = Column(String(25), primary_key=True)
    calibre = Column(String(25), primary_key=True)
    penetration = Column(Integer)
    damage = Column(Integer)
    velocity = Column(Integer)
    frag_pct = Column(Integer)

class Entry(Base): # Ammo Entry
    __tablename__ = 'entries'

    id = Column(Integer, primary_key=True, index=True)
    ammo_name = Column(String(25))
    calibre = Column(String(25))
    ammo_amount = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))

# storage model has a list of 