from flask import Blueprint, request, jsonify
from app.services.run_service import trigger_run, list_runs, get_run
from app.schemas import TaskSchema, TaskRunSchema
from app.services.task_services import (
    list_tasks as list_tasks_service,
    get_task as get_task_service,
    create_task as create_task_service,
    update_task as update_task_service,
    delete_task as delete_task_service,
)


# Define the API blueprint with /api prefix
api_bp = Blueprint("api", __name__, url_prefix="/api")

task_schema = TaskSchema()
task_list_schema = TaskSchema(many=True)


@api_bp.route("/tasks", methods=["GET"])
def list_tasks():
    tasks = list_tasks_service()
    result = task_list_schema.dump(tasks)
    return jsonify(result), 200


@api_bp.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = get_task_service(task_id)
    if not task:
        return jsonify({"message": "Task not found"}), 404
    result = task_schema.dump(task)
    return jsonify(result), 200


@api_bp.route("/tasks", methods=["POST"])
def create_task():
    json_data = request.get_json()
    if not json_data:
        return jsonify({"message": "No input data provided"}), 400

    data = task_schema.load(json_data)

    task = create_task_service(data)
    result = task_schema.dump(task)
    return jsonify(result), 201


@api_bp.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = get_task_service(task_id)
    if not task:
        return jsonify({"message": "Task not found"}), 404

    json_data = request.get_json()
    if not json_data:
        return jsonify({"message": "No input data provided"}), 400

    data = task_schema.load(json_data, partial=True)
    task = update_task_service(task, data)
    result = task_schema.dump(task)
    return jsonify(result), 200


@api_bp.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = get_task_service(task_id)
    if not task:
        return jsonify({"message": "Task not found"}), 404

    delete_task_service(task)
    return jsonify({"message": "Task deleted"}), 204


@api_bp.route("/tasks/<int:task_id>/run", methods=["POST"])
def run_task_now(task_id):
    run = trigger_run(task_id)
    if not run:
        return jsonify({"message": "Task not found"}), 404

    result = run_schema.dump(run)
    return jsonify(result), 200


run_schema = TaskRunSchema()
run_list_schema = TaskRunSchema(many=True)


@api_bp.route("/runs", methods=["GET"])
def list_task_runs():
    runs = list_runs()
    result = run_list_schema.dump(runs)
    return jsonify(result), 200


@api_bp.route("/runs/<int:run_id>", methods=["GET"])
def get_task_run(run_id):
    run = get_run(run_id)
    if not run:
        return jsonify({"message": "Run not found"}), 404

    result = run_schema.dump(run)
    return jsonify(result), 200
