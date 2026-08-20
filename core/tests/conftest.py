from fastapi.testclient import TestClient
from core.database import Base, create_engine, sessionmaker, get_db
from sqlalchemy import StaticPool
from main import app
import pytest
from users.models import UserModel
from tasks.models import TaskModel
from faker import Faker

fake = Faker()

SQLAlCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLAlCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass = StaticPool
)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope = "package")
def db_session():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope = "module", autouse = True)
def override_dependencies(db_session):
    app.dependency_overrides[get_db] = lambda: db_session
    yield
    app.dependency_overrides.pop(get_db, None)

@pytest.fixture(scope = "session", autouse = True)
def tear_up_and_down_database():
    Base.metadata.create_all(bind = engine)
    yield
    Base.metadata.drop_all(bind = engine)

@pytest.fixture(scope = "function")
def anon_client():
    client = TestClient(app)
    yield client

@pytest.fixture(scope = "package", autouse = True)
def generate_mock_data(db_session):
    user = UserModel(user_name = "usertest")
    user.set_password("12345678910")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    print(f"user created, username: {user.user_name}, ID: {user.id}")

    tasks_list = []
    for _ in range(10):
        tasks_list.append(
            TaskModel(
                user_id=user.id,
                title=fake.sentence(nb_words=8),
                description=fake.text(),
                is_completed=fake.boolean(),
            )
        )
    db_session.add_all(tasks_list)
    db_session.commit()
    print(f"added 10 tasks for the user with this user id: {user.id}")