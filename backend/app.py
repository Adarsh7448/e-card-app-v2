from flask import Flask
from application.config import LocalDevelopmentConfig
from application.database import db
from application.models import User
from application.security import jwt
from flask_cors import CORS
from application.celery_init import celery_init_app
from celery.schedules import crontab

app = None

def create_app():
    app = Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)
    # api.init_app(app)
    app.app_context().push()
    return app

app = create_app()
celery = celery_init_app(app)
celery.autodiscover_tasks()

@celery.on_after_finalize.connect 
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute = '*/2'),
        monthly_report.s(),
    )

from application.routes import *

if __name__ == "__main__":
    # db.create_all()
    # db.session.add(User(username="batman", email="batman@admin.com", password="123456", role = "admin"))
    # db.session.add(User(username="panther", email="panther@user.com", password="123456"))
    # db.session.commit()

    app.run()