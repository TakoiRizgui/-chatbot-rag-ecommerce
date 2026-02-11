"""
Script d'initialisation pour charger les données dans ChromaDB
"""

import sys
import os

# FIX: Ajouter le dossier parent au PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Maintenant l'import fonctionnera
from helpers.chromadb import get_rag_system


def main():
    """
    Charge le dataset et initialise la base vectorielle
    """
    print("=== Initialisation du système RAG ===\n")
    
    # Chemin vers le dataset
    dataset_path = "data/ecommerce_faq_dataset.csv"
    
    # Vérifier si le fichier existe
    if not os.path.exists(dataset_path):
        print(f"❌ Erreur: Le fichier {dataset_path} n'existe pas!")
        print(f"📥 Téléchargez le dataset et placez-le dans data/")
        
        # Vérifier d'autres emplacements
        if os.path.exists("../data/ecommerce_faq_dataset.csv"):
            dataset_path = "../data/ecommerce_faq_dataset.csv"
            print(f"✅ Trouvé à: {dataset_path}")
        elif os.path.exists("ecommerce_faq_dataset.csv"):
            dataset_path = "ecommerce_faq_dataset.csv"
            print(f"✅ Trouvé à: {dataset_path}")
        else:
            return
    
    # Récupérer le système RAG
    rag = get_rag_system()
    
    # Vérifier si la collection est déjà peuplée
    try:
        current_count = rag.get_collection_count()
        if current_count > 0:
            print(f"⚠️  La collection contient déjà {current_count} documents.")
            response = input("Voulez-vous la réinitialiser? (o/n): ")
            if response.lower() == 'o':
                # Supprimer l'ancienne collection et en créer une nouvelle
                rag.client.delete_collection(name=rag.collection_name)
                rag.initialize_chromadb()
                print("✅ Collection réinitialisée")
            else:
                print("❌ Initialisation annulée")
                return
    except Exception as e:
        print(f"⚠️  Erreur vérification: {e}")
        print("⚠️  Probablement collection vide, continuation...")
    
    # Charger le dataset
    print(f"📂 Chargement du dataset: {dataset_path}")
    df = rag.load_dataset(dataset_path)
    
    if df is None:
        print("❌ Erreur chargement dataset")
        return
    
    print(f"✅ Dataset chargé: {len(df)} lignes")
    print(f"📊 Colonnes: {list(df.columns)}")
    print(f"\n🔍 Aperçu:")
    print(df.head())
    
    # Peupler la base vectorielle
    print(f"\n💾 Insertion dans ChromaDB...")
    rag.populate_vectorstore(df)
    
    # Vérification
    final_count = rag.get_collection_count()
    print(f"\n✅ Initialisation terminée!")
    print(f"📊 Documents dans la base: {final_count}")
    
    # Test de recherche
    print(f"\n🧪 Test recherche...")
    test_query = "What payment methods do you accept?"
    results = rag.search_documents(test_query, n_results=3)
    
    print(f"\nQuery: {test_query}")
    print(f"Résultats: {len(results)}")
    if results:
        print(f"\nPremier résultat:")
        print(f"  Question: {results[0]['question']}")
        print(f"  Réponse: {results[0]['answer'][:100]}...")
    
    print(f"\n🎉 Système RAG prêt!")


if __name__ == "__main__":
    main()