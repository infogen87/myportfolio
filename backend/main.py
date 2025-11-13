from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import project_router, user_router
from models import ProjectsDB

from database import engine, Base


app = FastAPI()



origins = [
    "http://localhost",#change later
    "http://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])



app.include_router(project_router)
app.include_router(user_router)






Base.metadata.create_all(bind=engine) 
