

# 📚 Documentation Backend – Projet Bibliothèque

## 1️⃣ Informations générales

* **Technologies** : Flask (Python), SQLAlchemy, Marshmallow, Flask-Mail, APScheduler
* **Base de données** : SQLite (`library.db`)
* **Serveur** : [http://127.0.0.1:5000](http://127.0.0.1:5000)
* **Préfixe API** : `/api`
* **Mode** : Développement (`debug=True`)
* **Scheduler notifications** : toutes les 24h (modifiable via `Config.SCHEDULER_INTERVAL_MINUTES`)

---

## 2️⃣ Structure du projet

```
backend/
├─ .venv/                  # Environnement virtuel
├─ app.py                  # Serveur principal
├─ config.py               # Configurations Flask & Mail
├─ database.py             # SQLAlchemy & Marshmallow
├─ models.py               # Tables : User, Document, Emprunt, Notification
├─ schemas.py              # Conversion DB <-> JSON
├─ routes.py               # Routes API
├─ requirements.txt        # Dépendances Python
└─ .env                    # Variables secrètes (mail, clé, etc.)
```

---

## 3️⃣ Modèle de données (simplifié)

| Table          | Champs principaux                                                                | Description                              |
| -------------- | -------------------------------------------------------------------------------- | ---------------------------------------- |
| `User`         | id, nom, email, mot\_de\_passe                                                   | Utilisateurs de l’app                    |
| `Document`     | id, titre, auteur, categorie, statut                                             | Documents disponibles                    |
| `Emprunt`      | id, user\_id, document\_id, date\_emprunt, date\_retour, statut, renouvellements | Suivi des emprunts                       |
| `Notification` | id, user\_id, emprunt\_id, type, message, date\_notification                     | Notifications (rappel, échéance, retard) |

---

## 4️⃣ Endpoints API

### 4.1 Utilisateurs

| Endpoint     | Méthode | Description                  | Request JSON                                                        | Response JSON                                        |
| ------------ | ------- | ---------------------------- | ------------------------------------------------------------------- | ---------------------------------------------------- |
| `/api/users` | POST    | Créer un utilisateur         | `{ "nom":"Maxime", "email":"max@test.com", "mot_de_passe":"1234" }` | `{ "id":1, "nom":"Maxime", "email":"max@test.com" }` |
| `/api/users` | GET     | Lister tous les utilisateurs | —                                                                   | Liste JSON des utilisateurs                          |

---

### 4.2 Documents

| Endpoint         | Méthode | Description               | Request JSON                                                            | Response JSON            |
| ---------------- | ------- | ------------------------- | ----------------------------------------------------------------------- | ------------------------ |
| `/api/documents` | GET     | Lister tous les documents | —                                                                       | Liste JSON des documents |
| `/api/documents` | POST    | Ajouter un document       | `{ "titre":"Python", "auteur":"Auteur A", "categorie":"Informatique" }` | Document créé            |

---

### 4.3 Emprunts

| Endpoint                   | Méthode | Description           | Request JSON / Paramètres          | Response JSON                           |
| -------------------------- | ------- | --------------------- | ---------------------------------- | --------------------------------------- |
| `/api/emprunt`             | POST    | Créer un emprunt      | `{ "user_id":1, "document_id":2 }` | Emprunt créé                            |
| `/api/emprunt/<id>/renew`  | PUT     | Renouveler un emprunt | —                                  | Emprunt mis à jour                      |
| `/api/emprunt/<id>/return` | PUT     | Retourner un document | —                                  | Emprunt mis à jour, document disponible |
| `/api/emprunts`            | GET     | Lister les emprunts   | `?user_id=1` (optionnel)           | Liste JSON des emprunts                 |

---

### 4.4 Notifications

| Endpoint             | Méthode | Description          | Paramètres               | Response JSON                |
| -------------------- | ------- | -------------------- | ------------------------ | ---------------------------- |
| `/api/notifications` | GET     | Lister notifications | `?user_id=1` (optionnel) | Liste JSON des notifications |

**Types de notifications :**

* `rappel` → 2 jours avant la date de retour
* `echeance` → le jour de l’échéance
* `retard` → après la date limite

---

## 5️⃣ Règles métier importantes

* **Durée d’emprunt** : 7 jours
* **Renouvellement** : 1 seule fois, 7 jours supplémentaires
* **Retour** : doit être enregistré → document redevenu disponible
* **Disponibilité** : un document ne peut pas être emprunté par plusieurs utilisateurs simultanément
* **Notifications** : créées automatiquement par le scheduler

---

## 6️⃣ Exemple de flux pour le frontend

1. L’utilisateur se connecte / est créé via `/api/users`
2. Frontend liste les documents via `/api/documents`
3. L’utilisateur emprunte un document via `/api/emprunt`
4. Frontend affiche le statut et la date de retour
5. Scheduler génère notifications → frontend les récupère via `/api/notifications`
6. Utilisateur peut renouveler ou retourner un document via `/api/emprunt/<id>/renew` ou `/api/emprunt/<id>/return`

---

## 7️⃣ Notes pour l’équipe frontend

* Toutes les routes sont préfixées `/api`
* Les données sont envoyées et reçues en **JSON**
* Les dates sont au format ISO (`YYYY-MM-DD HH:MM:SS`)
* Le frontend doit gérer les statuts : `disponible`, `emprunte`, `en cours`, `terminé`, `en retard`

---

💡 **Conseil** : pour tester rapidement le backend avant de commencer le frontend, utilisez **Postman ou Insomnia**.

---
