import subprocess
import requests
import shutil
import os


def execute_task(task):
    """Dispatch execution based on task.type"""
    ttype = task.type
    config = task.config

    if ttype == "shell_command":
        return run_shell(config)

    if ttype == "http_request":
        return run_http(config)

    if ttype == "file_operation":
        return run_file_operation(config)

    raise ValueError(f"Unknown task type: {ttype}")


def run_shell(config):
    command = config.get("command")
    if not command:
        raise ValueError("Missing 'command' in config")

    result = subprocess.run(command, shell=True,
                            capture_output=True, text=True)
    logs = result.stdout + "\n" + result.stderr
    if result.returncode != 0:
        raise Exception(f"Shell command failed: {logs}")
    return logs


def run_http(config):
    url = config.get("url")
    method = config.get("method", "GET").upper()

    if not url:
        raise ValueError("Missing 'url' in config")

    response = requests.request(method, url)
    return f"Status: {response.status_code}\nBody: {response.text}"


def run_file_operation(config):
    op = config.get("operation")  # copy, move, delete
    src = config.get("source")
    dest = config.get("destination")

    if op == "copy":
        shutil.copy(src, dest)
        return f"Copied {src} to {dest}"

    if op == "move":
        shutil.move(src, dest)
        return f"Moved {src} to {dest}"

    if op == "delete":
        os.remove(src)
        return f"Deleted {src}"

    raise ValueError("Invalid file operation")
