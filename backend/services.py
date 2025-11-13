from schemas import ProjectCreate, ProjectResponse, ProjectUpdate, PaginatedProjectResponse
from uuid import UUID
from models import ProjectsDB
from fastapi import HTTPException
from sqlalchemy.orm import Session


class ProjectServices:
    @staticmethod
    def create_project(
        project_data: ProjectCreate,
        user_id: UUID,
        db: Session
    ) -> ProjectResponse:
        

        new_project = ProjectsDB(
            **project_data.model_dump(),
            user_id=user_id
        )
        db.add(new_project)
        db.commit()
        db.refresh(new_project)
        return ProjectResponse.model_validate(new_project)                                                                                                                           



    @staticmethod
    def update_project(
        project_data: ProjectUpdate,
        user_id: UUID,
        project_id: UUID,
        db: Session
    ) -> ProjectResponse:
        
        project = db.query(ProjectsDB).filter(
            ProjectsDB.id == project_id,
            ProjectsDB.user_id == user_id)
        
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        for key, value in project_data.model_dump(exclude_unset=True).items():
            setattr(project, key, value)


        return ProjectResponse.model_validate(project)


    @staticmethod
    def get_project(
        project_id: UUID,
        user_id: UUID,
        db: Session) -> ProjectResponse:

        project = db.query(ProjectsDB).filter(
            ProjectsDB.id == project_id,
            ProjectsDB.user_id == user_id)
        
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        return ProjectResponse.model_validate(project)


    @staticmethod
    def get_projects(
        *,
        user_id: UUID,
        limit: int = 10, 
        offset: int = 0,
        sort: str = "latest", 
        db: Session
    ) -> PaginatedProjectResponse:
        
        query = db.query(ProjectsDB).filter(ProjectsDB.user_id == user_id)

        if not query:
            raise HTTPException(status_code=404, detail="No Projects found")

        total = query.count()  
        # Sorting
        if sort == "latest":
            query = query.order_by(ProjectsDB.created_at.asc())
        else:
            query = query.order_by(ProjectsDB.created_at.desc())


        # Pagination
        projects = query.offset(offset).limit(limit).all()
        
        response = {
            "total": total,
            "limit": limit,
            "offset": offset,
            "results": [ProjectResponse.model_validate(project).model_dump() for project in projects]}
        return response




    @staticmethod
    def delete_project(
        
        project_id: UUID,
        db: Session,
        user_id: UUID) -> dict:
       

        project = db.query(ProjectsDB).filter(
            ProjectsDB.id == project_id,
            ProjectsDB.user_id == user_id).first()
    
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        db.delete(project)
        db.commit()
        return {"message": "Project deleted"}
        



project_services = ProjectServices()