from datetime import datetime

from app.extensions import db
from app.models import Task, TaskRun
from app.tasks.executor import execute_task


def trigger_run(task_id: int) -> TaskRun:
    task = Task.query.get(task_id)
    if not task:
        return None

    # Create initial run entry
    run = TaskRun(
        task_id=task.id,
        status="RUNNING",
        started_at=datetime.utcnow()
    )
    db.session.add(run)
    db.session.commit()

    # Execute task
    try:
        logs = execute_task(task)
        run.status = "SUCCESS"
        run.logs = logs
    except Exception as e:
        run.status = "FAILED"
        run.error_message = str(e)

    run.finished_at = datetime.utcnow()
    db.session.commit()

    return run


def list_runs() -> list[TaskRun]:
    return TaskRun.query.order_by(TaskRun.started_at.desc().nullslast()).all()


def get_run(run_id: int) -> TaskRun | None:
    return TaskRun.query.get(run_id)
