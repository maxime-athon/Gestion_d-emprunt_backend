from flask import Blueprint, request, jsonify
from database import db
from models import User, Document, Emprunt, Notification
from schemas import (
    user_schema, users_schema,
    document_schema, documents_schema,
    emprunt_schema, emprunts_schema,
    notification_schema, notifications_schema
)
from datetime import timedelta, datetime

api = Blueprint("api", __name__)

# ---------------- Users ----------------
@api.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    user = User(
        nom=data.get("nom"),
        email=data.get("email"),
        mot_de_passe=data.get("mot_de_passe")
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({
        "id": user.id,
        "nom": user.nom,
        "email": user.email,
        "mot_de_passe": user.mot_de_passe,
        "emprunts": [],
        "notifications": []
    }), 201

@api.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([
        {
            "id": u.id,
            "nom": u.nom,
            "email": u.email
        } for u in users
    ])


# ---------------- Documents ----------------
@api.route("/documents", methods=["GET"])
def list_documents():
    docs = Document.query.all()
    return documents_schema.jsonify(docs)

@api.route("/documents", methods=["POST"])
def create_document():
    data = request.get_json()
    if not data or not data.get("titre"):
        return jsonify({"error": "titre requis"}), 400
    doc = Document(titre=data["titre"], auteur=data.get("auteur"), categorie=data.get("categorie"))
    db.session.add(doc)
    db.session.commit()
    return document_schema.jsonify(doc), 201

# ---------------- Emprunts ----------------
@api.route("/emprunt", methods=["POST"])
def create_emprunt():
    data = request.get_json()
    user_id = data.get("user_id")
    document_id = data.get("document_id")
    if not user_id or not document_id:
        return jsonify({"error": "user_id et document_id requis"}), 400
    user = User.query.get(user_id)
    doc = Document.query.get(document_id)
    if not user or not doc:
        return jsonify({"error": "user ou document introuvable"}), 404
    if doc.statut != "disponible":
        return jsonify({"error": "document non disponible"}), 400
    emprunt = Emprunt(user_id=user.id, document_id=doc.id)
    doc.statut = "emprunte"
    db.session.add(emprunt)
    db.session.commit()
    return emprunt_schema.jsonify(emprunt), 201

@api.route("/emprunt/<int:id>/renew", methods=["PUT"])
def renew_emprunt(id):
    emprunt = Emprunt.query.get_or_404(id)
    # Règle métier : 1 renouvellement maximum
    if emprunt.renouvellements >= 1 or emprunt.statut != "en cours":
        return jsonify({"error": "Renouvellement impossible"}), 400
    emprunt.date_retour = emprunt.date_retour + timedelta(days=7)
    emprunt.renouvellements += 1
    db.session.commit()
    return emprunt_schema.jsonify(emprunt)

@api.route("/emprunt/<int:id>/return", methods=["PUT"])
def return_emprunt(id):
    emprunt = Emprunt.query.get_or_404(id)
    if emprunt.statut == "terminé":
        return jsonify({"message": "déjà retourné"}), 200
    emprunt.statut = "terminé"
    # rendre le document disponible
    doc = Document.query.get(emprunt.document_id)
    if doc:
        doc.statut = "disponible"
    db.session.commit()
    return emprunt_schema.jsonify(emprunt)

@api.route("/emprunts", methods=["GET"])
def list_emprunts():
    user_id = request.args.get("user_id", type=int)
    if user_id:
        emprunts = Emprunt.query.filter_by(user_id=user_id).all()
    else:
        emprunts = Emprunt.query.all()
    return emprunts_schema.jsonify(emprunts)

# ---------------- Notifications ----------------
@api.route("/notifications", methods=["GET"])
def list_notifications():
    user_id = request.args.get("user_id", type=int)
    if not user_id:
        return notifications_schema.jsonify(Notification.query.order_by(Notification.date_notification.desc()).all())
    notifs = Notification.query.filter_by(user_id=user_id).order_by(Notification.date_notification.desc()).all()
    return notifications_schema.jsonify(notifs)
