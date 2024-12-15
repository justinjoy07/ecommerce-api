import os
import time
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base

def create_app():
    app = Flask(__name__)
    test_mode = os.getenv("TESTING_MODE", "").lower() == "true"
    if test_mode:
        app.config['TESTING'] = True
    # Read the database URI from environment variables

    if test_mode:
        db_uri = "sqlite:///:memory:"
    else:
        db_uri = os.getenv('SQLALCHEMY_DATABASE_URI')
    if not db_uri:
        raise RuntimeError("Environment variable 'SQLALCHEMY_DATABASE_URI' not set")

    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    connect_db(app, retries=0)

    return app

def connect_db(app, retries):
    try:
        # Set up the database engine and session
        engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)

        # Initialize routes with a session instance
        from app.routes import init_routes
        init_routes(app, Session())
    except Exception as e:
        if retries < 5:
            retries = retries + 1
            time.sleep(2)
            connect_db(app, retries=retries)
        else:
            raise RuntimeError(f"Failed to initialize the app: {e}")


# If using the factory pattern, ensure this is set
app = create_app()