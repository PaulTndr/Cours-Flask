from marshmallow_sqlalchemy import ModelSchema

from .models import Task


class TaskSchema(ModelSchema):
    class Meta:
        model = Task
