from fastapi import FastAPI
from contextlib import asynccontextmanager
from tasks.routes import router as tasks_routes

tags_metadata = [
    {"name": "tasks",
                  "description": "Operations related to the task management",
                  "externalDocs":{
                      "description": "more about tasks",
                      "url": "http://example.com/docs/tasks"}
                      }
                      ]

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application Start Up")
    yield
    print("Application Shut Down")

app = FastAPI(
    title="ToDo Application",
    description="A description for ToDo Application",
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Mehdi Ostad",
        "url": "http://github.com/MehdiOstad1212",
        "email": "wishtree1248@gmail.com",
    },
    license_info={
        "name": "MIT",
    }, lifespan = lifespan, openapi_tags = tags_metadata)

app.include_router(tasks_routes)