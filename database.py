from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()  # Load the .env file

# export URL_DATABASE='postgresql://postgres.niqfgjqsjklhovgewfla:Dustinjohnson7@aws-0-us-east-1.pooler.supabase.com:6543/postgres'
URL_DATABASE = 'postgresql://postgres.niqfgjqsjklhovgewfla:Dustinjohnson7@aws-0-us-east-1.pooler.supabase.com:6543/postgres'
print(URL_DATABASE)

 
engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()