from typing import List, Optional

from app.extensions import db
from app.models import Task


def list_tasks() -> list[Task]:
    return Task.query.order_by(Task.created_at.desc()).all()


def get_task(task_id: int) -> Optional[Task]:
    return Task.query.get(task_id)


def create_task(data: dict) -> Task:
    task = Task(
        name=data["name"],
        type=data["type"],
        config=data["config"],
        enabled=data.get("enabled", True),
    )
    db.session.add(task)
    db.session.commit()
    return task


def update_task(task: Task, data: dict) -> Task:
    task.name = data.get("name", task.name)
    task.type = data.get("type", task.type)
    task.config = data.get("config", task.config)
    if "enabled" in data:
        task.enabled = data["enabled"]

    db.session.commit()
    return task


def delete_task(task: Task) -> None:
    db.session.delete(task)
    db.session.commit()
