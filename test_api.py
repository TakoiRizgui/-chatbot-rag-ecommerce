"""
Script de test pour vérifier le bon fonctionnement de l'API
"""

import requests
import json


def test_api():
    """
    Teste tous les endpoints de l'API
    """
    base_url = "http://localhost:8000"
    
    print("🧪 Test de l'API Chatbot RAG\n")
    print("=" * 60)
    
    # Test 1 : Route racine
    print("\n1️⃣  Test GET /")
    try:
        response = requests.get(f"{base_url}/")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {json.dumps(response.json(), indent=2)}")
        assert response.status_code == 200
        print("   ✅ Test réussi")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # Test 2 : Health check
    print("\n2️⃣  Test GET /health")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {json.dumps(response.json(), indent=2)}")
        assert response.status_code == 200
        print("   ✅ Test réussi")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # Test 3 : Stats
    print("\n3️⃣  Test GET /stats")
    try:
        response = requests.get(f"{base_url}/stats")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {json.dumps(response.json(), indent=2)}")
        assert response.status_code == 200
        print("   ✅ Test réussi")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # Test 4 : Recherche de documents
    print("\n4️⃣  Test POST /search")
    try:
        query_data = {
            "query": "What payment methods do you accept?",
            "n_results": 3
        }
        response = requests.post(
            f"{base_url}/search",
            json=query_data
        )
        print(f"   Status: {response.status_code}")
        result = response.json()
        print(f"   Query: {result['query']}")
        print(f"   Nombre de résultats: {result['n_results']}")
        if result['documents']:
            print(f"   Premier résultat:")
            print(f"     Question: {result['documents'][0]['question'][:80]}...")
            print(f"     Réponse: {result['documents'][0]['answer'][:80]}...")
        assert response.status_code == 200
        print("   ✅ Test réussi")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # Test 5 : Chat complet
    print("\n5️⃣  Test POST /chat")
    try:
        chat_data = {
            "query": "How can I track my order?"
        }
        response = requests.post(
            f"{base_url}/chat",
            json=chat_data
        )
        print(f"   Status: {response.status_code}")
        result = response.json()
        print(f"   Query: {result['query']}")
        print(f"   Nombre de documents récupérés: {len(result['top_documents'])}")
        print(f"   Réponse générée: {result['response'][:150]}...")
        assert response.status_code == 200
        print("   ✅ Test réussi")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    print("\n" + "=" * 60)
    print("\n🎉 Tous les tests sont terminés!")
    print("\n💡 Accédez à la documentation Swagger: http://localhost:8000/docs")


if __name__ == "__main__":
    test_api()