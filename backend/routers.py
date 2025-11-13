from typing import Annotated
from fastapi import APIRouter, status, Depends, Request
import schemas
from uuid import UUID
from sqlalchemy.orm import Session
from database import get_db
from services import project_services



project_router = APIRouter(prefix="/api/v1/projects", tags=["projects"])




@project_router.post("/", response_model=schemas.ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(
    project_data: schemas.ProjectCreate, 
    user_id: UUID = Depends(get_current_user_id),  
    db: Session = Depends(get_db)):  
    
    return project_services.create_project(
        project_data=project_data,
        user_id=user_id,
        db=db)



@project_router.patch("/{project_id}", response_model=schemas.ProjectResponse, status_code=status.HTTP_200_OK)
def update_project(
    request: Request,
    project_data: schemas.ProjectUpdate,
    user_id: UUID = Depends(get_current_user_id),  
    project_id: UUID,
    db: Session = Depends(get_db)):

    return project_services.update_project(
        project_id=project_id,
        project_data=project_data,
        user_id=user_id,
        db=db)


@project_router.get("/", response_model=schemas.PaginatedProjectResponse, status_code=status.HTTP_200_OK)
def get_all_projects(
    request: Request,
    user_id: UUID = Depends(get_current_user_id),  
    limit: int = 10, 
    offset: int = 0,
    sort: str = "latest", 
    db: Session = Depends(get_db)):

    return project_services.get_projects(
        user_id=user_id,
        limit=limit,
        offset=offset,
        sort=sort,
        db=db)



@project_router.get("/{project_id}", response_model=schemas.ProjectResponse, status_code=status.HTTP_200_OK)
def get_a_project(
    request: Request,
    project_id: UUID,
    user_id: UUID = Depends(get_current_user_id),  
    db: Session = Depends(get_db)):

    return project_services.get_project(
        project_id=project_id,
        user_id=user_id,
        db=db)




@project_router.delete("/{project_id}", response_model=dict, status_code=status.HTTP_200_OK)
def delete_project(
    project_id: UUID, 
    user_id: UUID = Depends(get_current_user_id),  
    db: Session = Depends(get_db)):

    return project_services.delete_project(
        project_id=project_id,
        user_id=user_id,
        db=db)





#-------------------users

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from schemas import UserCreate, UserResponse, UserUpdate
from services import user_service
from auth import get_current_user
from models import UserDB



user_router = APIRouter(prefix="/api/v1/users", tags=["users"])


@user_router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserCreate, 
    db: Session = Depends(get_db)):

    return user_service.create_user(user_data, db)


@user_router.get("/", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_user(
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)):

    return user_service.get_user(db, current_user.id)


@user_router.put("/", response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_user(
    updated_data: UserUpdate, 
    db: Session = Depends(get_db), 
    current_user: UserDB = Depends(get_current_user)):

    return user_service.update_user(updated_data, db, current_user.id)


@user_router.delete("/", response_model=dict, status_code=status.HTTP_200_OK)
def delete_user(
    db: Session = Depends(get_db), 
    current_user: UserDB = Depends(get_current_user)):

    return user_service.delete_user(db, current_user.id)  

