from database import db  # ✅ Import unique et partagé
from datetime import datetime

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mot_de_passe = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    emprunts = db.relationship('Emprunt', backref='user', lazy=True)
    notifications = db.relationship('Notification', backref='user', lazy=True)

class Document(db.Model):
    __tablename__ = 'document'

    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(200), nullable=False)
    auteur = db.Column(db.String(100), nullable=False)
    categorie = db.Column(db.String(100))
    statut = db.Column(db.String(50), default="disponible")

    emprunts = db.relationship('Emprunt', backref='document', lazy=True)

class Emprunt(db.Model):
    __tablename__ = 'emprunt'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    document_id = db.Column(db.Integer, db.ForeignKey('document.id'), nullable=False)
    date_emprunt = db.Column(db.DateTime, default=datetime.utcnow)
    date_retour = db.Column(db.DateTime)
    statut = db.Column(db.String(50), default="en cours")

    notifications = db.relationship('Notification', backref='emprunt', lazy=True)

class Notification(db.Model):
    __tablename__ = 'notification'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    emprunt_id = db.Column(db.Integer, db.ForeignKey('emprunt.id'), nullable=False)
    type = db.Column(db.String(50))  # rappel, echeance, retard
    message = db.Column(db.Text)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)