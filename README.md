# 🤖 Chatbot Intelligent E-commerce - Système RAG

Chatbot intelligent basé sur RAG (Retrieval Augmented Generation) pour répondre aux questions FAQ e-commerce.

## 📋 Table des matières

- [Architecture](#architecture)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [API Endpoints](#api-endpoints)
- [Docker](#docker)
- [Structure du projet](#structure-du-projet)
- [Démonstration](#démonstration)

## 🏗️ Architecture

Le projet est composé de plusieurs modules :
┌─────────────┐
│ Utilisateur│
└──────┬──────┘
│
▼
┌─────────────────┐
│ FastAPI │ (main.py)
│ Endpoints │
└────┬───────┬────┘
│ │
▼ ▼
┌─────────┐ ┌──────────┐
│ RAG │ │ LLM │
│ Module │ │Generator │
│(helpers)│ │ (llm.py) │
└────┬────┘ └────┬─────┘
│ │
▼ ▼
┌──────────┐ ┌─────────┐
│ChromaDB │ │ Gemini/ │
│(Vector DB)│ │ Fallback │
└──────────┘ └─────────┘


### Composants :

1. **FastAPI** : API REST exposant les endpoints
2. **RAG Module** : Gestion de ChromaDB et recherche vectorielle (`helpers/chromadb.py`)
3. **LLM Generator** : Génération de réponses avec Gemini ou mode fallback (`llm.py`)
4. **ChromaDB** : Base de données vectorielle pour la recherche sémantique

## 📦 Prérequis

- Python 3.11+
- Docker & Docker Compose (optionnel)
- Clé API Google Gemini (optionnel) : [Obtenir une clé](https://makersuite.google.com/app/apikey)

## 🚀 Installation

### Option 1 : Installation locale (Recommandée pour test rapide)

#### 1. Télécharger le projet

Téléchargez et extrayez le projet dans un dossier.

#### 2. Créer un environnement virtuel


# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
3. Installer les dépendances
bash
pip install -r requirements.txt
4. Télécharger le dataset
Téléchargez le dataset depuis Kaggle

Placez le fichier ecommerce_faq_dataset.csv dans le dossier data/

5. Initialiser la base de données

python -m helpers.init_data

6. Lancer l'API

uvicorn main:app --reload
L'API sera accessible sur : http://localhost:8000

Option 2 : Installation avec Docker
1. Télécharger le dataset
Placez ecommerce_faq_dataset.csv dans le dossier data/

2. Construire et lancer les conteneurs

docker-compose up --build

3. Initialiser les données (première fois uniquement)

docker-compose exec fastapi-app python -m helpers.init_data
L'API sera accessible sur : http://localhost:8000

📖 Utilisation
Accéder à la documentation Swagger
Ouvrez votre navigateur : http://localhost:8000/docs

Tester l'API avec curl

1. Route racine

curl http://localhost:8000/

2. Recherche de documents

curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "What payment methods do you accept?"}'

3. Chat complet

curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "How can I track my order?"}'
🔌 API Endpoints
GET /
Informations sur l'API

Réponse :


{
  "version": "1.0.0",
  "swagger": "/docs"
}
POST /search
Recherche les 5 documents les plus pertinents

Requête :


{
  "query": "What payment methods do you accept?",
  "n_results": 5
}
Réponse :


{
  "query": "What payment methods do you accept?",
  "n_results": 5,
  "documents": [
    {
      "document": "Question: ... Reponse: ...",
      "question": "...",
      "answer": "...",
      "distance": 0.25
    }
  ]
}
POST /chat
Endpoint principal : recherche + génération de réponse

Requête :


{
  "query": "How can I return a product?"
}
Réponse :


{
  "query": "How can I return a product?",
  "top_documents": [...],
  "response": "Pour retourner un produit..."
}
GET /stats
Statistiques de la base de données

Réponse :


{
  "total_documents": 79,
  "collection_name": "ecommerce_faq",
  "status": "active"
}
GET /health
Vérification de santé de l'API

Réponse :


{
  "status": "healthy",
  "service": "chatbot-rag-api"
}
🐳 Docker
Commandes utiles

# Lancer les services
docker-compose up -d

# Voir les logs
docker-compose logs -f

# Arrêter les services
docker-compose down

# Reconstruire l'image
docker-compose up --build

# Accéder au conteneur
docker-compose exec fastapi-app bash

# Initialiser les données
docker-compose exec fastapi-app python -m helpers.init_data
Volumes persistants
Les données ChromaDB sont persistées dans le dossier ./data/chroma_langchain_db grâce aux volumes Docker.

📁 Structure du projet

chatbot_rag_project/
│
├── 📂 data/                           # Données
│   ├── chroma_langchain_db/          # Base ChromaDB persistée
│   └── ecommerce_faq_dataset.csv     # Dataset (à télécharger)
│
├── 📂 helpers/                        # Modules utilitaires
│   ├── chromadb.py                   # Module RAG (ChromaDB)
│   └── init_data.py                  # Script d'initialisation
│
├── main.py                           # API FastAPI principale
├── llm.py                            # Générateur LLM (Gemini)
├── requirements.txt                  # Dépendances Python
├── Dockerfile                        # Configuration Docker
├── docker-compose.yml                # Orchestration Docker
├── .env.example                      # Template variables d'environnement
├── .dockerignore                     # Fichiers ignorés par Docker
├── README.md                         # Documentation principale
├── DEMONSTRATION.md                  # Guide de démonstration
├── QUICKSTART.md                     # Guide démarrage rapide
├── test_api.py                       # Tests automatisés
└── setup.py                          # Script de setup (optionnel)
🎬 Démonstration
Pour une démonstration détaillée pas à pas, consultez le fichier DEMONSTRATION.md.

Test rapide en 2 minutes :

# 1. Installer
pip install -r requirements.txt

# 2. Initialiser (répondre 'o' si demandé)
python -m helpers.init_data

# 3. Lancer
uvicorn main:app --reload

# 4. Tester dans le navigateur
# http://localhost:8000/docs
🔧 Configuration
Utiliser Google Gemini (optionnel)
Obtenez une clé API sur Google AI Studio

Créez un fichier .env à partir du template :


cp .env.example .env
Éditez .env et ajoutez votre clé :

env
GOOGLE_API_KEY=votre_cle_api_ici
Mode Fallback
Si Gemini n'est pas configuré, le système utilise automatiquement un mode fallback qui retourne la réponse du document le plus pertinent.

🎯 Fonctionnalités
✅ Chargement et indexation de 79 FAQ e-commerce
✅ Recherche vectorielle avec ChromaDB
✅ Génération de réponses avec LLM (Gemini + Fallback)
✅ API REST avec FastAPI
✅ Documentation Swagger automatique
✅ Dockerisation complète
✅ Persistance des données
✅ Tests automatisés
✅ Documentation exhaustive

📝 Notes techniques
Le système utilise ChromaDB en mode PersistentClient pour la persistance

Les embeddings sont générés automatiquement par ChromaDB (all-MiniLM-L6-v2)

La base de données est stockée dans data/chroma_langchain_db/

L'API suit les standards REST avec validation Pydantic

🧪 Tests
Exécutez les tests automatisés :


python test_api.py
Ou testez manuellement via Swagger UI : http://localhost:8000/docs

🤝 Contribution
Ce projet a été réalisé dans le cadre d'un examen. Pour toute question, contactez l'auteur.

📄 Licence
MIT License

Auteur : Takoi RIZGUI
Date : 04-02-2026
Examen : Chatbot Intelligent - Système RAG

Pour une démonstration complète, exécutez python -m helpers.init_data puis uvicorn main:app --reload et accédez à http://localhost:8000/docs



## 📝 **Changements apportés :**

1. **Mise à jour de l'architecture** : Montre la nouvelle structure avec `helpers/`
2. **Correction des chemins** : `data/chroma_langchain_db` au lieu de `chroma_db`
3. **Mise à jour des commandes** : `python -m helpers.init_data` au lieu de `python init_data.py`
4. **Ajout de la section Démonstration** : Lien vers `DEMONSTRATION.md`
5. **Structure du projet** : Montre la nouvelle organisation
6. **Notes techniques** : Informations sur ChromaDB et embeddings
7. **Instructions clarifiées** : Pour l'enseignant qui teste

## 🎯 **Pour l'enseignant :**

Avec ce `README.md` mis à jour, l'enseignant peut :
1. Comprendre la nouvelle structure
2. Suivre les bonnes commandes
3. Tester rapidement avec la section "Démonstration"
4. Accéder à toutes les informations nécessaires