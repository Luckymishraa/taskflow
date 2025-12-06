from marshmallow import Schema, fields, validates, ValidationError

ALLOWED_TASK_TYPES = {"shell_command", "http_request", "file_operation"}


class TaskSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    type = fields.Str(required=True)
    config = fields.Dict(required=True)
    enabled = fields.Bool(load_default=True)

    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @validates("type")
    def validate_type(self, value, **kwargs):
        if value not in ALLOWED_TASK_TYPES:
            raise ValidationError(f"type must be one of {ALLOWED_TASK_TYPES}")


class TaskRunSchema(Schema):
    id = fields.Int(dump_only=True)
    task_id = fields.Int(required=True)
    status = fields.Str(dump_only=True)
    logs = fields.Str(dump_only=True)
    error_message = fields.Str(dump_only=True)
    started_at = fields.DateTime(dump_only=True)
    finished_at = fields.DateTime(dump_only=True)
