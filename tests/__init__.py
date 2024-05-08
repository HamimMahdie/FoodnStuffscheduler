# app/__init__.py or somewhere inside the app module

from flask import Flask

def create_app(config=None):
    app = Flask(__name__)
    if config:
        app.config.update(config)
    
    # Initialize other parts of the app
    from .routes import init_routes
    init_routes(app)
    
    return app
