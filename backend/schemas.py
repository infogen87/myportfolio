# schemas.py
from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime
from uuid import UUID
from typing import Optional, List

# Tool Schemas
class ToolBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)

class ToolCreate(ToolBase):
    pass

class ToolResponse(ToolBase):
    id: UUID
    project_id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Project Schemas
class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1)
    github_link: Optional[str] = Field(None, max_length=500)
    live_link: Optional[str] = Field(None, max_length=500)

class ProjectCreate(ProjectBase):
    tools: List[str] = Field(default_factory=list)

class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, min_length=1)
    github_link: Optional[str] = Field(None, max_length=500)
    live_link: Optional[str] = Field(None, max_length=500)
    tools: Optional[List[str]] = None

class ProjectResponse(ProjectBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    tools: List[ToolResponse] = []
    
    class Config:
        from_attributes = True


# Skill Schemas
class SkillBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)

class SkillCreate(SkillBase):
    pass

class SkillUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)

class SkillResponse(SkillBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
