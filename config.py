import os

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    # DB : utilise DATABASE_URL si défini sinon sqlite local
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///" + os.path.join(BASE_DIR, "library.db"))
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Sécurité
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

    # Mail
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "True").lower() in ("true", "1", "yes")
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "athonmaxime@gmail.com")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "BM142006$")

    # Scheduler interval (en minutes) : par défaut 1440 (24h)
    SCHEDULER_INTERVAL_MINUTES = int(os.getenv("SCHEDULER_INTERVAL_MINUTES", "1440"))