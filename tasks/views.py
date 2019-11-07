from flask.views import MethodView
from flask_smorest import Blueprint, abort
from ..app import db
from .models import Task
from .serializers import TaskSchema

task_blueprint = Blueprint(
    "tasks", "tasks", url_prefix="/tasks", description="Operations on tasks"
)

@task_blueprint.route("/")
class Tasks(MethodView):
    @task_blueprint.response(TaskSchema(many=True))
    def get(self):
        """List tasks"""
        return Task.query.all()

    @task_blueprint.arguments(TaskSchema(only=["title"]))
    @task_blueprint.response(TaskSchema, code=201)
    def post(self, new_data):
        """Creates a new task"""
        try:
            db.session.add(new_data)
            db.session.commit()
            return new_data
        except:
            db.session.rollback()
            abort(400, message=f"An error occured")

@task_blueprint.route("/<task_id>")
class TasksById(MethodView):
    @task_blueprint.response(TaskSchema)
    def get(self, task_id):
        """Get task by ID"""
        return Task.query.get_or_404(task_id)

    @task_blueprint.arguments(TaskSchema(only=["title", "done"]))
    @task_blueprint.response(TaskSchema)
    def put(self, update_data, task_id):
        """Update existing task"""
        try:

            task = Task.query.get_or_404(task_id)
            task.title = update_data.title
            db.session.commit()
            return update_data
        except:
            db.session.rollback()
            abort(400, message=f"An error occured")

    @task_blueprint.response(code=204)
    def delete(self, task_id):
        """Delete task"""
        task = Task.query.get_or_404(task_id)
        db.session.delete(task)

