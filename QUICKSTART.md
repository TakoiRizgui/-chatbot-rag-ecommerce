QUICKSTART.md

# 🚀 Test Rapide - Chatbot RAG

## Test en 1 minute

```bash
# 1. Installer
pip install -r requirements.txt

# 2. Initialiser (dataset déjà fourni)
python -m helpers.init_data

# 3. Lancer
uvicorn main:app --reload

# 4. Tester
# http://localhost:8000/docs
Commandes essentielles
Installation

# Créer environnement
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Installer dépendances
pip install -r requirements.txt
Lancement

# Lancer l'API
uvicorn main:app --reload

# Tester
curl http://localhost:8000/
# ou ouvrir http://localhost:8000/docs
Tests

# Tests automatisés
python test_api.py

# Test manuel
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "How can I track my order?"}'
Fichiers importants
main.py : API FastAPI

helpers/chromadb.py : Module RAG

llm.py : Génération réponses

data/ecommerce_faq_dataset.csv : Dataset

Problèmes fréquents
Port occupé ? --port 8001

Dataset manquant ? Il est fourni dans data/

Réinitialiser : python -m helpers.init_data

Pour tester : http://localhost:8000/docs
Auteur : Takoi RIZGUI
Examen : Chatbot Intelligent RAG



---

## `README.md` (Version courte pour examen)

```markdown
# Chatbot RAG E-commerce

## Description
Chatbot intelligent basé sur RAG (Retrieval Augmented Generation) répondant aux FAQ e-commerce.

## Installation

pip install -r requirements.txt
python -m helpers.init_data
uvicorn main:app --reload
Structure

projet/
├── data/                    # Dataset + ChromaDB
├── helpers/                 # Modules RAG
├── main.py                  # API FastAPI
├── llm.py                   # Génération LLM
└── requirements.txt         # Dépendances
Endpoints API
GET / : Informations

POST /search : Recherche documents

POST /chat : Chat complet

GET /docs : Documentation Swagger

Docker 

docker-compose up --build
docker-compose exec fastapi-app python -m helpers.init_data



Takoi RIZGUI - Examen Chatbot Intelligent
