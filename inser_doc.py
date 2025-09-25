import requests

documents = [
    {"titre": "Radio et Innovation", "auteur": "Auteur VIII", "categorie": "Média"},
    {"titre": "Transformation Numérique", "auteur": "Auteur IX", "categorie": "Stratégie"},
    {"titre": "Design UX/UI", "auteur": "Auteur X", "categorie": "Design"},
    {"titre": "SQL pour les Développeurs", "auteur": "Auteur XI", "categorie": "Base de données"},
    {"titre": "Sécurité Web", "auteur": "Auteur XII", "categorie": "Cybersécurité"},
    {"titre": "Programmation Orientée Objet", "auteur": "Auteur XIII", "categorie": "Concepts"},
    {"titre": "JavaScript Moderne", "auteur": "Auteur XIV", "categorie": "Frontend"},
    {"titre": "React.js Dynamique", "auteur": "Auteur XV", "categorie": "Framework"},
    {"titre": "Docker Simplifié", "auteur": "Auteur XVI", "categorie": "DevOps"},
    {"titre": "Méthodes de Documentation", "auteur": "Auteur XVII", "categorie": "Qualité"},
    {"titre": "Leadership Communautaire", "auteur": "Auteur XVIII", "categorie": "Engagement"},
    {"titre": "Structuration de Modules", "auteur": "Auteur XIX", "categorie": "Architecture"},
    {"titre": "Valorisation Locale", "auteur": "Auteur XX", "categorie": "Territoire"},
    {"titre": "Introduction à la culture Kabyè", "auteur": "Kodjo T.", "categorie": "Culture"},
    {"titre": "Guide du numérique rural", "auteur": "Maxime A.", "categorie": "Stratégie"},
    {"titre": "Histoire de la Foire D’Kwowô", "auteur": "Afi K.", "categorie": "Territoire"},
    {"titre": "Stratégies de mobilisation locale", "auteur": "Balakyèm M.", "categorie": "Engagement"},
    {"titre": "Valorisation du terroir togolais", "auteur": "Yendoube S.", "categorie": "Territoire"},
    {"titre": "Architecture Vue.js immersive", "auteur": "Maxime A.", "categorie": "Frontend"},
    {"titre": "Gestion de projet communautaire", "auteur": "Djamila B.", "categorie": "Management"},
    {"titre": "Documentation professionnelle", "auteur": "Kossi N.", "categorie": "Qualité"},
    {"titre": "API REST et intégration locale", "auteur": "Maxime A.", "categorie": "Backend"},
    {"titre": "Guide du storytelling digital", "auteur": "Amina T.", "categorie": "Communication"},
    {"titre": "Sécurité des plateformes web", "auteur": "Jean-Paul D.", "categorie": "Cybersécurité"},
    {"titre": "Mobilisation des jeunes", "auteur": "Mariam S.", "categorie": "Engagement"},
    {"titre": "Création d’interfaces inclusives", "auteur": "Maxime A.", "categorie": "Design"},
    {"titre": "Vue.js pour les événements", "auteur": "Koffi E.", "categorie": "Frontend"},
    {"titre": "Python et Flask pour les projets", "auteur": "Balakyèm M.", "categorie": "Backend"},
    {"titre": "Gestion des rôles et accès", "auteur": "Nadine K.", "categorie": "Architecture"},
    {"titre": "Renforcement communautaire", "auteur": "Maxime A.", "categorie": "Engagement"},
    {"titre": "Export PDF et démonstration", "auteur": "Yao T.", "categorie": "Qualité"},
    {"titre": "Connexion et inscription fluide", "auteur": "Maxime A.", "categorie": "Frontend"},
    {"titre": "Vue admin et valorisation", "auteur": "Balakyèm M.", "categorie": "Architecture"}
]

for doc in documents:
    doc["statut"] = "disponible"
    res = requests.post("http://127.0.0.1:5000/api/documents", json=doc)
    print(f"📚 {doc['titre']} → {res.status_code}")