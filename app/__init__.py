from flask import Flask
from flask_bootstrap import Bootstrap5
from .models import db
from .routes import main

def create_app():
    app = Flask(__name__)
    bootstrap = Bootstrap5(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

    # Fehlerbehandlung hinzufügen, falls benötigt
    @app.errorhandler(404)
    def not_found_error(error):
        return "Page not found", 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return "Internal server error", 500
    
    # Eventuelle weitere Konfigurationen oder Initialisierungen
    #
    ##
    ###
    ##
    #
    # Rückgabe der App-Instanz
    return app
