
from typing import Annotated, List
from fastapi import FastAPI, HTTPException, Depends, status, BackgroundTasks
from sqlmodel import Field, SQLModel, Session
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select as async_select
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager
# cqrs: segregate write and read operations
# dependency injection

@asynccontextmanager
async def lifespan(app:FastAPI):
    async with engine.begin() as conn:

        await conn.run_sync(SQLModel.metadata.create_all)
    
    yield

app = FastAPI(lifespan=lifespan)

# Async database setup
DATABASE_URl = "mysql+pymysql://root:Dustinjohnson7@localhost:3306/Tarkov_Project"
engine = create_async_engine(DATABASE_URl, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Models
class UserBase(SQLModel): # username and ID
    username: str

class UserCreate(UserBase):
    pass

class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)

class UserRead(UserBase):
    id: int

# Service Layer
class UserService:
    async def create_item(self, username: UserCreate, db: Session) -> User:
        db_user = User(username=User.username)
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user
    
    async def get_user(self, user_id: int, db: Session) -> User:
        async with db as session:
            statement = async_select(User).where(User.id == user_id)
            result = await session.execute(statement)
            user = result.scalar()
            return user
        
    async def get_user(self, db: Session) -> List[User]:
        async with db as session:
            statement = async_select(User)
            result = await session.execute(statement)
            users = result.scalar().all()
            return users
        
def get_db() -> AsyncSession: # dont have db open too long
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user_service():
    return UserService()

db_dependency = Annotated[Session, Depends(get_db)]
user_service_dependency = Annotated[Session, Depends(get_user_service)]

# API Layer
@app.post("/users/", response_model=UserRead)
async def create_user(user: UserCreate, background_tasks: BackgroundTasks, user_service: user_service_dependency, db: db_dependency):
    created_user = await user_service.create_user(user, db)
    background_tasks.add_task(log_operation, user_id=created_user.id)
    return created_user

@app.get("/users/", response_model=List[UserRead])
async def read_users(db: db_dependency, user_service: user_service_dependency):
    users = await user_service.get_users(db)
    return users

@app.get("/users/{user_id}", response_model=UserRead)
async def read_user(user_id: int, db: db_dependency, user_service: user_service_dependency):
    user = await user_service.get_user(user_id, db)
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")

