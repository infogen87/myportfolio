from typing import Literal, Optional
from pydantic import BaseModel, ConfigDict, EmailStr
from uuid import UUID
from datetime import datetime



class ProjectCreate(BaseModel):
    name: str
    description: str
    github_link: str
    live_link: str



class ProjectResponse(BaseModel):
    id: UUID
    owner_id: UUID
    name: str
    description: str
    github_link: str
    live_link: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)



class ProjectUpdate(BaseModel):
    name: Optional[str] = None  
    description: Optional[str] = None  
    github_link: Optional[str] = None  
    live_link: Optional[str] = None  


class PaginatedProjectResponse(BaseModel):
    total: int
    limit: int
    offset: int
    results: list[ProjectResponse]        






#----------------------------users


class UserBase(BaseModel):
    username: str
    password: str

    
class UserCreate(UserBase):
    pass 


class UserResponse(BaseModel):
    id: UUID
    username: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        # orm_mode = True
        from_attributes = True
        


class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None

