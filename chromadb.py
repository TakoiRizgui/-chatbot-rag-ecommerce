import pandas as pd
import chromadb  # Import standard
import json
from typing import List, Dict
import os


class RAGSystem:
    """
    Système RAG complet pour le chatbot e-commerce
    """
    
    def __init__(self, collection_name: str = "ecommerce_faq"):
        """
        Initialise le système RAG avec ChromaDB
        """
        self.collection_name = collection_name
        self.client = None
        self.collection = None
        self.initialize_chromadb()
    
    def initialize_chromadb(self):
        """
        Initialise la connexion à ChromaDB
        """
        # Chemin selon la structure recommandée
        chroma_path = "./data/chroma_langchain_db"
        
        # Créer le dossier si nécessaire
        os.makedirs(chroma_path, exist_ok=True)
        
        # Utiliser chromadb (sans alias)
        self.client = chromadb.PersistentClient(path=chroma_path)
        
        try:
            self.collection = self.client.get_collection(name=self.collection_name)
            print(f"✅ Collection '{self.collection_name}' chargée")
        except:
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"description": "FAQ E-commerce chatbot"}
            )
            print(f"✅ Collection '{self.collection_name}' créée")
    
    def load_dataset(self, file_path: str) -> pd.DataFrame:
        """
        Charge le dataset FAQ depuis JSON ou CSV
        """
        print(f"📂 Chargement du dataset: {file_path}")
        
        # Vérifier si le fichier existe
        if not os.path.exists(file_path):
            print(f"❌ Fichier non trouvé: {file_path}")
            return None
        
        # Essayer de charger comme JSON d'abord
        try:
            print("   Tentative de chargement JSON...")
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Extraire les questions et réponses
            if 'questions' in data and isinstance(data['questions'], list):
                questions = []
                answers = []
                
                for item in data['questions']:
                    if 'question' in item and 'answer' in item:
                        questions.append(item['question'])
                        answers.append(item['answer'])
                
                df = pd.DataFrame({
                    'Questions': questions,
                    'Answers': answers
                })
                
                print(f"✅ JSON chargé: {len(df)} entrées")
                return df
            
        except json.JSONDecodeError:
            print("   ⚠️  Pas un JSON, tentative CSV...")
        except Exception as e:
            print(f"   ⚠️  Erreur JSON: {e}")
        
        # Si JSON échoue, essayer CSV
        try:
            print("   Tentative de chargement CSV...")
            df = pd.read_csv(file_path, encoding='utf-8', on_bad_lines='skip')
            
            # Détecter les colonnes
            question_col = None
            answer_col = None
            
            for col in df.columns:
                col_lower = col.lower().strip()
                if 'question' in col_lower:
                    question_col = col
                if 'answer' in col_lower:
                    answer_col = col
            
            if question_col and answer_col:
                df = df.rename(columns={question_col: 'Questions', answer_col: 'Answers'})
                df = df.dropna(subset=['Questions', 'Answers'])
                df = df[df['Questions'].str.strip() != '']
                df = df[df['Answers'].str.strip() != '']
                
                print(f"✅ CSV chargé: {len(df)} entrées")
                return df
            
        except Exception as e:
            print(f"   ❌ Erreur CSV: {e}")
        
        print(f"❌ Impossible de charger")
        return None
    
    def populate_vectorstore(self, df: pd.DataFrame):
        """
        Remplit la base vectorielle
        """
        if df is None or df.empty:
            print("❌ DataFrame vide")
            return
        
        print(f"📝 Préparation de {len(df)} documents...")
        
        documents = []
        metadatas = []
        ids = []
        
        for idx, row in df.iterrows():
            doc_text = f"Question: {row['Questions']}\nReponse: {row['Answers']}"
            documents.append(doc_text)
            
            metadatas.append({
                "question": str(row['Questions']),
                "answer": str(row['Answers']),
                "index": int(idx)
            })
            
            ids.append(f"doc_{idx}")
        
        # Insérer par lots
        batch_size = 50
        total = len(documents)
        
        for i in range(0, total, batch_size):
            batch_docs = documents[i:i+batch_size]
            batch_metas = metadatas[i:i+batch_size]
            batch_ids = ids[i:i+batch_size]
            
            self.collection.add(
                documents=batch_docs,
                metadatas=batch_metas,
                ids=batch_ids
            )
            
            progress = min(i+batch_size, total)
            print(f"   📝 Inséré: {progress}/{total}")
        
        print(f"✅ {total} documents insérés")
    
    def search_documents(self, query: str, n_results: int = 5) -> List[Dict]:
        """
        Recherche les documents pertinents
        """
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            formatted_results = []
            if results['documents'] and results['documents'][0]:
                for i in range(len(results['documents'][0])):
                    formatted_results.append({
                        "document": results['documents'][0][i],
                        "question": results['metadatas'][0][i]['question'],
                        "answer": results['metadatas'][0][i]['answer'],
                        "distance": results['distances'][0][i] if 'distances' in results else None
                    })
            
            return formatted_results
            
        except Exception as e:
            print(f"❌ Erreur recherche: {e}")
            return []
    
    def get_collection_count(self) -> int:
        """
        Nombre de documents
        """
        try:
            return self.collection.count()
        except:
            return 0


# Instance globale
rag_system = None


def get_rag_system() -> RAGSystem:
    """
    Retourne l'instance globale
    """
    global rag_system
    if rag_system is None:
        rag_system = RAGSystem()
    return rag_system