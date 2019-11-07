from flask import template_rendered
import pytest
from flask_sqlalchemy import SQLAlchemy
from app import create_app, db

@pytest.fixture
def user_name():
    return "paul"


@pytest.fixture
def app():
    app = create_app()
    return app

@pytest.fixture
def captured_templates(app):
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))

    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)

@pytest.fixture(scope='session')
def app(request):
    app = create_app()
    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app

@pytest.fixture(scope='session')
def _db(app):
    db.create_all()
    return db
