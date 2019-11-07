import os

from flask import Flask, render_template

from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy()

from flask_marshmallow import Marshmallow
from flask_smorest import Api, Blueprint, abort

ma = Marshmallow()


def create_app():
    app = Flask(__name__)
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = f"sqlite:///{os.path.join(basedir, 'data.sqlite')}"
    app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
    app.config["OPENAPI_VERSION"] = "3.0.2"
    app.config["OPENAPI_URL_PREFIX"] = "openapi"
    app.config["API_VERSION"] = "1"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "api"
    app.config["OPENAPI_SWAGGER_UI_VERSION"] = "3.23.11"

    db.init_app(app)

    from .tasks.serializers import TaskSchema
    from .tasks.models import Task

    api = Api(app)
    ma.init_app(app)
    from .tasks.views import task_blueprint
    api.register_blueprint(task_blueprint)

    migrate = Migrate(app, db)

    @app.route('/')
    def index():
        return render_template('index.html')


    @app.route('/user/<name>')
    def user(name):
        return render_template('user.html', name=name)

    @app.route('/professor/<sex>')
    def getProfessorBySex(sex):
        if sex!="F" and sex!="M":
            sex="None"
        return {
            "name": "Paul",
            "birthday": "02 January",
            "age": 85,
            "sex": sex,
            "friends": ["Amadou", "Mariam"]
        }

    @app.route('/todos')
    def getAllTasks():
        """On get toutes les task"""
        tasks = Task.query.all()
        return {"results": TaskSchema(many=True).dump(tasks)}

    return app