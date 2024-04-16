from sqlalchemy import Boolean, Column, Integer, String
from database import Base

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

class UpdateAmmo(Base): # filter by if post.ammo_name = tarkov_ammo.ammo_name & post.calibre = tarkov_ammo.calibre 
                  # -> post.tarkov_ammo.penetration etc
    __tablename__ = 'updates'

    id = Column(Integer, primary_key=True, index=True)
    ammo_name = Column(String(25))
    calibre = Column(String(25))
    ammo_amount = Column(Integer)
    user_id = Column(Integer)



