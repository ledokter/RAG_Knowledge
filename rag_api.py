from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import sys
import os

# Ajout du chemin courant pour l'import local
sys.path.append(os.path.dirname(__file__))
from rag_engine import KnowledgeBase

app = FastAPI(title="Local RAG API", description="API pour interroger le disque D: Knowledge Base")
kb = KnowledgeBase()

class SearchQuery(BaseModel):
    query: str
    category: str = "all"
    limit: int = 5

@app.get("/")
def read_root():
    return {"status": "online", "message": "RAG Engine Ready on D:"}

@app.post("/search")
def search(q: SearchQuery):
    """Recherche générique"""
    return kb.unified_search(q.query)

@app.post("/search/stackoverflow")
def search_so(q: SearchQuery):
    return kb.search_stackoverflow(q.query, q.limit)

@app.post("/search/docs")
def search_docs(q: SearchQuery):
    return kb.search_docs_by_category(q.query, q.category, q.limit)

if __name__ == "__main__":
    print("🚀 Démarrage du serveur API RAG sur http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
