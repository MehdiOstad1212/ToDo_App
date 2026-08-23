from fastapi import FastAPI, Depends, Request, Response, status, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from contextlib import asynccontextmanager
from tasks.routes import router as tasks_routes
from users.routes import router as users_routes
from users.models import UserModel
from datetime import datetime, timedelta
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
import time
import random
import httpx

scheduler = AsyncIOScheduler()

def my_tast():
    print(f"Task executed at: {time.strftime("%Y-%m-%d %H:%M:%S")}")


tags_metadata = [
    {
        "name": "tasks",
        "description": "Operations related to the task management",
        "externalDocs": {
            "description": "more about tasks",
            "url": "http://example.com/docs/tasks",
        },
    }
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application Start Up")
    scheduler.add_job(my_tast, IntervalTrigger(seconds = 1000))
    scheduler.start()
    yield
    print("Application Shut Down")
    scheduler.shutdown()


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
    },
    lifespan=lifespan,
    openapi_tags=tags_metadata,
)

app.include_router(tasks_routes)
app.include_router(users_routes)


from auth.jwt_auth import get_authenticated_user


@app.get("/public")
def public_route():
    return {"message": "This is a public route."}


@app.get("/private")
def private_route(user=Depends(get_authenticated_user)):
    print(user.user_name)
    return {"message": "This is a private route."}


@app.get("/set-cookie")
def set_cookie(response: Response):
    expires = datetime.utcnow() + timedelta(days=7)
    response.set_cookie(
        key="test",
        value="something",
        httponly=True,
        secure=True,
        samesite="Lax",
    )
    return {"message": "Cookie has been set successfully"}


@app.get("/get-cookie")
def get_cookie(request: Request):
    print(request.cookies.get("test"))
    return {"message": "Cookie has been requested and sent successfully"}


@app.delete("/delete-cookie")
def delete_cookie(response: Response):
    response.delete_cookie(key="test")
    return {"message": "Cookie has been removed!"}


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


origins = ["http://127.0.0.1:5500"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    error_response = {
        "error": True,
        "status_code": exc.status_code,
        "detail": str(exc.detail)
    }
    return JSONResponse(status_code = exc.status_code, content = error_response)

@app.exception_handler(RequestValidationError)
async def http_validation_exception_handler(request, exc):
    error_response = {
        "error": True,
        "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
        "detail": "there was a problem with your form request",
        "content": exc.errors()
    }
    return JSONResponse(status_code = status.HTTP_422_UNPROCESSABLE_CONTENT, 
                        content = error_response)

task_counter = 1

def start_task(task_id):
    print("start the task")
    print(f"doing the process: {task_id}")
    time.sleep(random.randint(5,25))
    print(f"finished the task: {task_id}")

@app.get("/initiate-task", status_code = 200)
async def initiate_task(background_tasks: BackgroundTasks):
    global task_counter
    background_tasks.add_task(start_task, task_id = task_counter)
    task_counter += 1
    return JSONResponse({"detail": "task is done"})

from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache

cache_backend = InMemoryBackend()
FastAPICache.init(cache_backend)

async def request_current_weather (latitude: float, longitude: float):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m"
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params = params)
    if response.status_code == 200:
        data = response.json()
        current_weather = data.get("current", {})
        return current_weather
    else:
        return None

@app.get("/fetch-weather", status_code = 200)
#@cache(expire = 10)
async def fetch_current_weather(latitude: float = 40.7128,
                                longitude: float = -74.0060):
    catch_key = f"weather-{latitude}-{longitude}"
    catched_data = await cache_backend.get(catch_key)
    if catched_data:
            return JSONResponse(content = {"current_weather": catched_data})
    current_weather = await request_current_weather(latitude, longitude)
    if current_weather:
        await cache_backend.set(catch_key, current_weather, 10)
        return JSONResponse(content = {"current_weather": current_weather})
    else:
        return JSONResponse(content = {"detail": "Failed to fetch weather"},
                            status_code = 500)