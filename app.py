import os

from flask import Flask, render_template

from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data.sqlite')}"
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

    db.init_app(app)

    from .tasks.serializers import TaskSchema
    from .tasks.models import Task

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