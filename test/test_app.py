from flask import Flask
from ..tasks.tests.factories import TaskFactory

def test_app(app):
    assert app is not None
    assert isinstance(app, Flask)


def test_index_route(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "ECM" in response.get_data(as_text=True)


def test_index_user(client, user_name):
    response = client.get(f"/user/{user_name}")
    assert response.status_code == 200
    assert f"{user_name}" in response.get_data(as_text=True)


def test_user_template(app, client, user_name):
    response = client.get(f"/user/{user_name}")
    template = app.jinja_env.get_template('user.html')
    assert template.render(name=user_name) == response.get_data(as_text=True)

def test_professor_view(app, client):
    response = client.get("/professor/F")
    assert response.json["name"] == "Paul"
    assert response.json["sex"] == "F"

def test_todos(app, client, db_session):
    task = TaskFactory()
    db_session.commit()

    response = client.get("/todos")
    assert len(response.json["results"]) > 0