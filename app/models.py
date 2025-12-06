from datetime import datetime

from .extensions import db


class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    config = db.Column(db.JSON, nullable=False)
    enabled = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class TaskRun(db.Model):
    __tablename__ = "task_runs"
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey("tasks.id"), nullable=False)

    # PENDING, RUNNING, SUCCESS, FAILED
    status = db.Column(db.String(20), default="PENDING")
    logs = db.Column(db.Text)
    error_message = db.Column(db.Text)

    started_at = db.Column(db.DateTime)
    finished_at = db.Column(db.DateTime)

    task = db.relationship("Task", backref="runs")
