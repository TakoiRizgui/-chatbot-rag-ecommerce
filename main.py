from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import uvicorn
from helpers.chromadb import get_rag_system
from llm import get_llm_generator

# Créer l'application FastAPI
app = FastAPI(
    title="Chatbot Intelligent E-commerce",
    description="API RAG pour un chatbot FAQ e-commerce",
    version="1.0.0"
)


# Modèles Pydantic pour la validation des données
class SearchQuery(BaseModel):
    query: str
    n_results: Optional[int] = 5


class ChatQuery(BaseModel):
    query: str


class ChatResponse(BaseModel):
    query: str
    top_documents: List[Dict]
    response: str


# ENDPOINT 1 : Route racine
@app.get("/")
async def root():
    """
    Endpoint racine retournant les informations de l'API
    """
    return {
        "version": "1.0.0",
        "swagger": "/docs"
    }


# ENDPOINT 2 : Recherche de documents
@app.post("/search")
async def search_documents(search_query: SearchQuery):
    """
    Recherche les documents les plus pertinents pour une requête
    
    Args:
        search_query: Objet contenant la requête et le nombre de résultats souhaités
        
    Returns:
        Liste des documents les plus pertinents
    """
    try:
        rag = get_rag_system()
        results = rag.search_documents(
            query=search_query.query,
            n_results=search_query.n_results
        )
        
        return {
            "query": search_query.query,
            "n_results": len(results),
            "documents": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la recherche: {str(e)}")


# ENDPOINT 3 : Chat complet (recherche + génération)
@app.post("/chat", response_model=ChatResponse)
async def chat(chat_query: ChatQuery):
    """
    Endpoint principal du chatbot : recherche des documents pertinents 
    et génère une réponse complète
    
    Args:
        chat_query: Objet contenant la question de l'utilisateur
        
    Returns:
        Réponse complète avec la query, les documents et la réponse générée
    """
    try:
        # Récupérer le système RAG et le générateur LLM
        rag = get_rag_system()
        llm = get_llm_generator()
        
        # Rechercher les documents pertinents
        top_documents = rag.search_documents(
            query=chat_query.query,
            n_results=5
        )
        
        # Générer la réponse
        generated_response = llm.generate_response(
            query=chat_query.query,
            top_documents=top_documents
        )
        
        return ChatResponse(
            query=chat_query.query,
            top_documents=top_documents,
            response=generated_response
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du chat: {str(e)}")


# ENDPOINT 4 : Statistiques de la base de données
@app.get("/stats")
async def get_stats():
    """
    Retourne des statistiques sur la base de données vectorielle
    """
    try:
        rag = get_rag_system()
        count = rag.get_collection_count()
        
        return {
            "total_documents": count,
            "collection_name": rag.collection_name,
            "status": "active"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des stats: {str(e)}")


# ENDPOINT 5 : Santé de l'application
@app.get("/health")
async def health_check():
    """
    Vérifie l'état de santé de l'application
    """
    return {
        "status": "healthy",
        "service": "chatbot-rag-api"
    }


if __name__ == "__main__":
    # Lancer le serveur
    uvicorn.run(app, host="0.0.0.0", port=8000)