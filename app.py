import os
from flask import Flask
from config import Config
from flask_mail import Mail, Message
from flask_cors import CORS
from flask_migrate import Migrate
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import joinedload

# 📦 Modules internes
from database import db, ma
from models import Emprunt, Notification, User, Document
from routes import api

# 🏗️ Initialisation de l'application Flask
app = Flask(__name__)
app.config.from_object(Config)

# 🔌 Initialisation des extensions
db.init_app(app)
ma.init_app(app)
mail = Mail(app)
CORS(app, resources={r"/api/*": {"origins": "*"}})
migrate = Migrate(app, db)

# 🔗 Enregistrement du blueprint
app.register_blueprint(api, url_prefix="/api")

# 🗃️ Création des tables au démarrage
with app.app_context():
    db.create_all()

# 🔔 Crée une notification si elle n'existe pas déjà
def create_notification_if_missing(user_id, emprunt_id, notif_type, message):
    exists = Notification.query.filter_by(user_id=user_id, emprunt_id=emprunt_id, type=notif_type).first()
    if exists:
        return None
    n = Notification(user_id=user_id, emprunt_id=emprunt_id, type=notif_type, message=message)
    db.session.add(n)
    db.session.commit()
    return n

# 📧 Envoie un e-mail si les identifiants sont configurés
def send_mail(to_email, subject, body):
    if not app.config.get("MAIL_USERNAME") or not app.config.get("MAIL_PASSWORD"):
        app.logger.warning("Mail credentials not configured; skipping send_mail")
        return False
    try:
        msg = Message(subject=subject,
                      sender=app.config["MAIL_USERNAME"],
                      recipients=[to_email],
                      body=body)
        mail.send(msg)
        return True
    except Exception as e:
        app.logger.error(f"Erreur envoi mail: {e}")
        return False

# ⏰ Vérifie les emprunts et génère les notifications
def check_overdue_and_send_notifications():
    with app.app_context():
        now = datetime.utcnow()
        emprunts = Emprunt.query.options(
            joinedload(Emprunt.document),
            joinedload(Emprunt.user)
        ).filter(Emprunt.statut == "en cours").all()

        for e in emprunts:
            # 🕒 Rappel : dans les 3 prochaines minutes
            if 0 < (e.date_retour - now).total_seconds() <= 180:
                message = f"Rappel : votre emprunt du document '{e.document.titre}' arrive à échéance le {e.date_retour.date()}."
                create_notification_if_missing(e.user_id, e.id, "rappel", message)
                send_mail(e.user.email, "Rappel de retour - bibliothèque", message)

            # 📅 Échéance : aujourd’hui
            if e.date_retour.date() == now.date():
                message = f"Échéance : votre emprunt du document '{e.document.titre}' est dû aujourd'hui ({e.date_retour.date()})."
                create_notification_if_missing(e.user_id, e.id, "echeance", message)
                send_mail(e.user.email, "Échéance emprunt - bibliothèque", message)

            # ⛔ Retard : date dépassée
            if e.date_retour < now:
                if e.statut != "en retard":
                    e.statut = "en retard"
                    db.session.commit()
                message = f"Retard : votre emprunt du document '{e.document.titre}' était dû le {e.date_retour.date()}."
                create_notification_if_missing(e.user_id, e.id, "retard", message)
                send_mail(e.user.email, "Retard de retour - bibliothèque", message)

# 🔁 Planification automatique
scheduler = BackgroundScheduler()
scheduler.add_job(func=check_overdue_and_send_notifications, trigger="interval", minutes=1)
scheduler.start()

# 🚀 Lancement de l'application
if __name__ == "__main__":
    with app.app_context():
        check_overdue_and_send_notifications()  # ✅ Exécution immédiate
    app.run(debug=True)