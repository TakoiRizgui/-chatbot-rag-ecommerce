FROM python:3.11-slim

WORKDIR /app

# Installer uniquement les dépendances ESSENTIELLES
RUN pip install --no-cache-dir \
    fastapi==0.104.1 \
    uvicorn==0.24.0 \
    chromadb==0.4.18 \
    pandas==2.1.3 \
    google-generativeai==0.3.1 \
    python-dotenv==1.0.0 \
    pydantic==2.5.0

# ChromaDB utilise ses propres embeddings, pas besoin de sentence-transformers

# Créer la structure de dossiers
RUN mkdir -p /app/data/chroma_langchain_db

# Copier le code
COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
