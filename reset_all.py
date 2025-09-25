from app import app
from database import db
from models import User, Document, Emprunt, Notification

with app.app_context():
    # 🔥 Supprime toutes les données
    db.session.query(Notification).delete()
    db.session.query(Emprunt).delete()
    db.session.query(Document).delete()
    db.session.query(User).delete()
    db.session.commit()

    print("✅ Toutes les données ont été supprimées. La base est vide.")