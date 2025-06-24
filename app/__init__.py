from flask import Flask
from flask_bootstrap import Bootstrap5

def create_app():
    app = Flask(__name__)
    bootstrap = Bootstrap5(app)


    # Konfiguration laden
    app.config.from_object("app.config.Config")
    
    # Blueprints/Routes registrieren
    from app.routes import main
    app.register_blueprint(main)

    # Datenbank initialisieren und Tabellen erstellen
    from app.models import db
    db.init_app(app)
    with app.app_context():
        db.create_all()  # Erstellt die Tabellen in der Datenbank, falls sie nicht existieren

    # Eventuelle weitere Initialisierungen hier


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
