import os
from typing import List, Dict
import google.generativeai as genai
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()


class LLMGenerator:
    """
    Générateur de réponses utilisant un LLM (Gemini par défaut)
    """
    
    def __init__(self, use_gemini: bool = True):
        """
        Initialise le générateur LLM
        
        Args:
            use_gemini: Si True, utilise Google Gemini, sinon mode simulation
        """
        self.use_gemini = use_gemini
        
        if self.use_gemini:
            api_key = os.getenv("GOOGLE_API_KEY")
            if api_key and api_key != "votre_cle_api_ici":
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel('gemini-pro')
                print("Gemini initialisé avec succès")
            else:
                print("Clé API Gemini non configurée, passage en mode simulation")
                self.use_gemini = False
    
    def generate_response(self, query: str, top_documents: List[Dict]) -> str:
        """
        Génère une réponse basée sur la question et les documents récupérés
        
        Args:
            query: Question de l'utilisateur
            top_documents: Liste des 5 documents les plus pertinents
            
        Returns:
            Réponse générée par le LLM
        """
        # Construire le contexte à partir des documents
        context = self._build_context(top_documents)
        
        # Créer le prompt
        prompt = self._create_prompt(query, context)
        
        if self.use_gemini:
            try:
                response = self.model.generate_content(prompt)
                return response.text
            except Exception as e:
                print(f"Erreur lors de la génération avec Gemini: {e}")
                return self._generate_fallback_response(query, top_documents)
        else:
            return self._generate_fallback_response(query, top_documents)
    
    def _build_context(self, top_documents: List[Dict]) -> str:
        """
        Construit le contexte à partir des documents récupérés
        """
        context_parts = []
        for i, doc in enumerate(top_documents, 1):
            context_parts.append(f"Document {i}:")
            context_parts.append(f"Question: {doc['question']}")
            context_parts.append(f"Réponse: {doc['answer']}")
            context_parts.append("")
        
        return "\n".join(context_parts)
    
    def _create_prompt(self, query: str, context: str) -> str:
        """
        Crée le prompt pour le LLM
        """
        prompt = f"""Tu es un assistant e-commerce intelligent. 
Réponds à la question de l'utilisateur en te basant UNIQUEMENT sur les informations fournies dans le contexte ci-dessous.

Contexte (FAQ E-commerce):
{context}

Question de l'utilisateur: {query}

Instructions:
- Réponds de manière claire et concise
- Utilise uniquement les informations du contexte
- Si la réponse n'est pas dans le contexte, dis que tu n'as pas cette information
- Sois professionnel et courtois

Réponse:"""
        
        return prompt
    
    def _generate_fallback_response(self, query: str, top_documents: List[Dict]) -> str:
        """
        Génère une réponse de secours si Gemini n'est pas disponible
        Retourne simplement la réponse du document le plus pertinent
        """
        if top_documents and len(top_documents) > 0:
            best_match = top_documents[0]
            return f"Basé sur notre FAQ: {best_match['answer']}"
        else:
            return "Je n'ai pas trouvé d'information pertinente pour répondre à votre question."


# Instance globale du générateur
llm_generator = None


def get_llm_generator() -> LLMGenerator:
    """
    Retourne l'instance globale du générateur LLM (singleton)
    """
    global llm_generator
    if llm_generator is None:
        llm_generator = LLMGenerator()
    return llm_generator