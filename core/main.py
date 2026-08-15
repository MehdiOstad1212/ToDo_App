from fastapi import FastAPI, Depends, Request, Response
from contextlib import asynccontextmanager
from tasks.routes import router as tasks_routes
from users.routes import router as users_routes
from users.models import UserModel
from datetime import datetime, timedelta
from fastapi.middleware.cors import CORSMiddleware
import time

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


from auth.jwt_auth import get_authenticated_user

@app.get("/public")
def public_route():
    return {"message": "This is a public route."}

@app.get("/private")
def private_route(user = Depends(get_authenticated_user)):
    print(user.user_name)
    return {"message": "This is a private route."}


@app.get("/set-cookie")
def set_cookie(response : Response):
    expires = datetime.utcnow() + timedelta(days=7)
    response.set_cookie(key = "test", value = "something",
                        httponly=True, secure=True, samesite="Lax")
    return {"message" : "Cookie has been set successfully"}

@app.get("/get-cookie")
def get_cookie(request : Request):
    print(request.cookies.get("test"))
    return {"message" : "Cookie has been requested and sent successfully"}

@app.delete("/delete-cookie")
def delete_cookie(response : Response):
    response.delete_cookie(key = "test")
    return {"message" : "Cookie has been removed!"}


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

origins = [
    "http://127.0.0.1:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)