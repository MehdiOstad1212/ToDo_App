from core.database import SessionLocal
from sqlalchemy.orm import Session
from users.models import UserModel
from tasks.models import TaskModel
from faker import Faker

fake = Faker()


def main():
    db = SessionLocal()
    try:
        user = seed_users(db)
        seed_tasks(db, user)
    finally:
        db.close()


def seed_users(db):
    user = UserModel(user_name=fake.user_name())
    user.set_password("159753")
    db.add(user)
    db.commit()
    db.refresh(user)
    print(f"user created, username: {user.user_name}, ID: {user.id}")
    return user


def seed_tasks(db, user, count=10):
    tasks_list = []
    for _ in range(count):
        tasks_list.append(
            TaskModel(
                user_id=user.id,
                title=fake.sentence(nb_words=8),
                description=fake.text(),
                is_completed=fake.boolean(),
            )
        )
    db.add_all(tasks_list)
    db.commit()
    print(f"added 10 tasks for the user with this user id: {user.id}")


if __name__ == "__main__":
    main()
