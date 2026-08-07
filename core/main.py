from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from tasks.routes import router as tasks_routes
from users.routes import router as users_routes
from users.models import UserModel

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
app.include_router(users_routes)


from fastapi.security import APIKeyQuery

query_schema = APIKeyQuery(name = "x-key")

@app.get("/public")
def public_route():
    return {"message": "This is a public route."}

@app.get("/private")
def private_route(api_key = Depends(query_schema)):
    print(api_key)
    return {"message": "This is a private route."}