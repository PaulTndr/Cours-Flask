import datetime

from ..app import db


class Task(db.Model):
    __tablename__ = 'Task'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True, index=True)
    creation_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    done = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return self.title