import os
from flask import Flask
from config import Config
from database import db, ma
from routes import api
from flask_mail import Mail, Message
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from models import Emprunt, Notification, User, Document

# optionnel: charger .env si tu utilises python-dotenv
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

# extensions
db.init_app(app)
ma.init_app(app)
mail = Mail(app)

# register blueprint
app.register_blueprint(api, url_prefix="/api")

# create tables
with app.app_context():
    db.create_all()

# Fonction qui crée une notification en DB (évite doublons par type+emprunt)
def create_notification_if_missing(user_id, emprunt_id, notif_type, message):
    exists = Notification.query.filter_by(user_id=user_id, emprunt_id=emprunt_id, type=notif_type).first()
    if exists:
        return None
    n = Notification(user_id=user_id, emprunt_id=emprunt_id, type=notif_type, message=message)
    db.session.add(n)
    db.session.commit()
    return n

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

def check_overdue_and_send_notifications():
    with app.app_context():
        now = datetime.utcnow()
        emprunts = Emprunt.query.filter(Emprunt.statut == "en cours").all()
        for e in emprunts:
            days_left = (e.date_retour - now).days
            # Rappel 2 jours avant
            if 0 < (e.date_retour - now).total_seconds() <= 2 * 24 * 3600:
                # crée rappel s'il n'existe pas
                message = f"Rappel : votre emprunt du document '{e.document.titre}' arrive à échéance le {e.date_retour.date()}."
                create_notification_if_missing(e.user_id, e.id, "rappel", message)
                # envoi mail
                send_mail(e.user.email, "Rappel de retour - bibliothèque", message)
            # jour J -> échéance
            if e.date_retour.date() == now.date():
                message = f"Echéance : votre emprunt du document '{e.document.titre}' est dû aujourd'hui ({e.date_retour.date()})."
                create_notification_if_missing(e.user_id, e.id, "echeance", message)
                send_mail(e.user.email, "Echéance emprunt - bibliothèque", message)
            # en retard
            if e.date_retour < now:
                # marque en retard si nécessaire
                if e.statut != "en retard":
                    e.statut = "en retard"
                    db.session.commit()
                message = f"Retard : votre emprunt du document '{e.document.titre}' était dû le {e.date_retour.date()}."
                create_notification_if_missing(e.user_id, e.id, "retard", message)
                send_mail(e.user.email, "Retard de retour - bibliothèque", message)

# Scheduler
scheduler = BackgroundScheduler()
interval_min = app.config.get("SCHEDULER_INTERVAL_MINUTES", 1440)
scheduler.add_job(func=check_overdue_and_send_notifications, trigger="interval", minutes=interval_min)
scheduler.start()

if __name__ == "__main__":
    # utile pour dev; en prod, lancer avec gunicorn/uwsgi
    app.run(debug=True)
