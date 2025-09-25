from flask import Blueprint, request, jsonify
from models import db, User, Document, Emprunt, Notification
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

api = Blueprint('api', __name__)

# 🔐 Inscription
@api.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email déjà utilisé"}), 409

    hashed_pw = generate_password_hash(data['mot_de_passe'])
    user = User(
        nom=data['nom'],
        email=data['email'],
        mot_de_passe=hashed_pw,
        is_admin=data.get('is_admin', False)
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Inscription réussie"}), 201

# 🔐 Connexion
@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and check_password_hash(user.mot_de_passe, data['mot_de_passe']):
        return jsonify({
            "message": "Connexion réussie",
            "user_id": user.id,
            "nom": user.nom,
            "is_admin": user.is_admin
        }), 200
    return jsonify({"error": "Identifiants invalides"}), 401

# 👤 Liste des utilisateurs avec leurs emprunts
@api.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    result = []
    for u in users:
        emprunts = []
        for e in u.emprunts:
            emprunts.append({
                "id": e.id,
                "statut": e.statut,
                "date_retour": e.date_retour,
                "document": {
                    "id": e.document.id,
                    "titre": e.document.titre,
                    "auteur": e.document.auteur
                }
            })
        result.append({
            "id": u.id,
            "nom": u.nom,
            "email": u.email,
            "emprunts": emprunts
        })
    return jsonify(result)

# 📚 Liste des documents
@api.route('/documents', methods=['GET'])
def get_documents():
    docs = Document.query.all()
    return jsonify([{
        "id": d.id,
        "titre": d.titre,
        "auteur": d.auteur,
        "categorie": d.categorie,
        "statut": d.statut
    } for d in docs])

# 📥 Ajouter un document
@api.route('/documents', methods=['POST'])
def add_document():
    data = request.get_json()
    doc = Document(
        titre=data['titre'],
        auteur=data['auteur'],
        categorie=data.get('categorie', ''),
        statut='disponible'
    )
    db.session.add(doc)
    db.session.commit()
    return jsonify({"message": "Document ajouté"}), 201

# 📦 Emprunter un document
@api.route('/emprunt', methods=['POST'])
def emprunter():
    data = request.get_json()
    doc = Document.query.get(data['document_id'])
    if not doc or doc.statut != 'disponible':
        return jsonify({"error": "Document non disponible"}), 400

    emprunt = Emprunt(
        user_id=data['user_id'],
        document_id=data['document_id'],
        date_emprunt=datetime.utcnow(),
        date_retour=datetime.utcnow() + timedelta(days= 7),
        statut='en cours'
    )
    doc.statut = 'emprunté'
    db.session.add(emprunt)
    db.session.commit()
    return jsonify({"message": "Emprunt effectué"}), 201

# 🔔 Notifications par utilisateur
@api.route('/notifications', methods=['GET'])
def get_notifications():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify([])

    notifs = Notification.query.filter_by(user_id=user_id).all()
    return jsonify([{
        "id": n.id,
        "type": n.type,
        "message": n.message,
        "emprunt_id": n.emprunt_id
    } for n in notifs])

@api.route('/profil/<int:user_id>', methods=['GET'])
def get_profil(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Utilisateur introuvable"}), 404

    emprunts = [{
        "id": e.id,
        "statut": e.statut,
        "date_emprunt": e.date_emprunt,
        "date_retour": e.date_retour,
        "document": {
            "id": e.document.id,
            "titre": e.document.titre,
            "auteur": e.document.auteur
        }
    } for e in user.emprunts]

    notifications = [{
        "id": n.id,
        "type": n.type,
        "message": n.message,
        "date_creation": n.date_creation,
        "emprunt_id": n.emprunt_id
    } for n in user.notifications]

    return jsonify({
        "id": user.id,
        "nom": user.nom,
        "email": user.email,
        "is_admin": user.is_admin,
        "emprunts": emprunts,
        "notifications": notifications
    })
@api.route('/admin/data', methods=['GET'])
def get_admin_data():
    user_id = request.args.get('user_id')
    user = User.query.get(user_id)
    if not user or not user.is_admin:
        return jsonify({"error": "Accès refusé"}), 403

    users = User.query.all()
    result = []
    for u in users:
        emprunts = [{
            "titre": e.document.titre,
            "statut": e.statut,
            "date_retour": e.date_retour
        } for e in u.emprunts]
        result.append({
            "nom": u.nom,
            "email": u.email,
            "emprunts": emprunts
        })
    return jsonify(result)