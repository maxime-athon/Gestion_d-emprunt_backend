from datetime import datetime, timedelta
from database import db

# ---------- User ----------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mot_de_passe = db.Column(db.String(255), nullable=False)  # stocker hash en prod
    emprunts = db.relationship('Emprunt', backref='user', lazy=True)
    notifications = db.relationship('Notification', backref='user', lazy=True)

# ---------- Document ----------
class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(255), nullable=False)
    auteur = db.Column(db.String(255))
    categorie = db.Column(db.String(100))
    statut = db.Column(db.String(50), default='disponible')  # 'disponible' | 'emprunte'
    emprunts = db.relationship('Emprunt', backref='document', lazy=True)

# ---------- Emprunt ----------
class Emprunt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_emprunt = db.Column(db.DateTime, default=datetime.utcnow)
    date_retour = db.Column(db.DateTime)
    statut = db.Column(db.String(50), default='en cours')  # en cours, en retard, terminé
    renouvellements = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    document_id = db.Column(db.Integer, db.ForeignKey('document.id'), nullable=False)

    def __init__(self, user_id, document_id, duree=7):
        self.user_id = user_id
        self.document_id = document_id
        self.date_emprunt = datetime.utcnow()
        self.date_retour = self.date_emprunt + timedelta(days=duree)

# ---------- Notification ----------
class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(500))
    date_notification = db.Column(db.DateTime, default=datetime.utcnow)
    type = db.Column(db.String(50))  # rappel, echeance, retard
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    emprunt_id = db.Column(db.Integer, db.ForeignKey('emprunt.id'), nullable=True)  # optionnel
