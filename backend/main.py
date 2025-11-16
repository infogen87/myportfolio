# main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import os
from dotenv import load_dotenv
from uuid import UUID
from datetime import datetime
from contextlib import asynccontextmanager

from database import get_db, create_tables
from models import Project, Tool, Skill
from schemas import (
    ProjectCreate, ProjectUpdate, ProjectResponse,
    SkillCreate, SkillUpdate, SkillResponse
)

load_dotenv()

# Get USER_ID from environment
USER_ID = UUID(os.getenv("USER_ID"))

# Create tables on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables
    create_tables()
    yield
    # Shutdown: Add cleanup code here if needed

app = FastAPI(
    title="Portfolio API",
    description="API for managing portfolio projects and skills",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================== PROJECT ENDPOINTS ====================

@app.post("/projects", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED, tags=["projects"])
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    """Create a new project with tools"""
    db_project = Project(
        user_id=USER_ID,
        name=project.name,
        description=project.description,
        github_link=project.github_link,
        live_link=project.live_link
    )
    db.add(db_project)
    db.flush()  # Get the project ID before adding tools
    
    # Add tools
    for tool_name in project.tools:
        db_tool = Tool(project_id=db_project.id, name=tool_name)
        db.add(db_tool)
    
    db.commit()
    db.refresh(db_project)
    return db_project


@app.get("/projects", response_model=List[ProjectResponse], tags=["projects"])
def get_all_projects(db: Session = Depends(get_db)):
    """Get all projects"""
    projects = db.query(Project).filter(Project.user_id == USER_ID).all()
    return projects


@app.get("/projects/{project_id}", response_model=ProjectResponse, tags=["projects"])
def get_project(project_id: UUID, db: Session = Depends(get_db)):
    """Get a single project by ID"""
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == USER_ID
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return project


@app.put("/projects/{project_id}", response_model=ProjectResponse, tags=["projects"])
def update_project(project_id: UUID, project_update: ProjectUpdate, db: Session = Depends(get_db)):
    """Update a project"""
    db_project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == USER_ID
    ).first()
    
    if not db_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Update project fields
    update_data = project_update.model_dump(exclude_unset=True, exclude={"tools"})
    for field, value in update_data.items():
        setattr(db_project, field, value)
    
    db_project.updated_at = datetime.utcnow()
    
    # Update tools if provided
    if project_update.tools is not None:
        # Delete existing tools
        db.query(Tool).filter(Tool.project_id == project_id).delete()
        
        # Add new tools
        for tool_name in project_update.tools:
            db_tool = Tool(project_id=db_project.id, name=tool_name)
            db.add(db_tool)
    
    db.commit()
    db.refresh(db_project)
    return db_project


@app.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["projects"])
def delete_project(project_id: UUID, db: Session = Depends(get_db)):
    """Delete a project"""
    db_project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == USER_ID
    ).first()
    
    if not db_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    db.delete(db_project)
    db.commit()
    return None


# ==================== SKILL ENDPOINTS ====================

@app.post("/skills", response_model=SkillResponse, status_code=status.HTTP_201_CREATED, tags=["skills"])
def create_skill(skill: SkillCreate, db: Session = Depends(get_db)):
    """Create a new skill"""
    db_skill = Skill(
        user_id=USER_ID,
        name=skill.name
    )
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    return db_skill


@app.get("/skills", response_model=List[SkillResponse], tags=["skills"])
def get_all_skills(db: Session = Depends(get_db)):
    """Get all skills"""
    skills = db.query(Skill).filter(Skill.user_id == USER_ID).all()
    return skills


@app.get("/skills/{skill_id}", response_model=SkillResponse, tags=["skills"])
def get_skill(skill_id: UUID, db: Session = Depends(get_db)):
    """Get a single skill by ID"""
    skill = db.query(Skill).filter(
        Skill.id == skill_id,
        Skill.user_id == USER_ID
    ).first()
    
    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found"
        )
    return skill


@app.put("/skills/{skill_id}", response_model=SkillResponse, tags=["skills"])
def update_skill(skill_id: UUID, skill_update: SkillUpdate, db: Session = Depends(get_db)):
    """Update a skill"""
    db_skill = db.query(Skill).filter(
        Skill.id == skill_id,
        Skill.user_id == USER_ID
    ).first()
    
    if not db_skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found"
        )
    
    update_data = skill_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_skill, field, value)
    
    db_skill.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_skill)
    return db_skill


@app.delete("/skills/{skill_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["skills"])
def delete_skill(skill_id: UUID, db: Session = Depends(get_db)):
    """Delete a skill"""
    db_skill = db.query(Skill).filter(
        Skill.id == skill_id,
        Skill.user_id == USER_ID
    ).first()
    
    if not db_skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found"
        )
    
    db.delete(db_skill)
    db.commit()
    return None


# ==================== HEALTH CHECK ====================

@app.get("/", tags=["health"])
def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "message": "Portfolio API is running",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)