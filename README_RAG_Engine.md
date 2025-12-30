# 🧠 Moteur RAG & API

Ce dossier contient l'intelligence du système RAG. Il permet d'interroger la base de données brute située sur `D:\RAG_Knowledge`.

## 🛠️ Composition
*   **`rag_engine.py`** : La librairie Python "cœur". Elle sait comment ouvrir la base SQLite StackOverflow et comment scanner les fichiers textes (Markdown/Code) pour trouver des mots-clés.
*   **`rag_api.py`** : Un serveur Web (FastAPI) qui expose le moteur via une API HTTP REST standard.

## 🚀 Utilisation

### 1. Mode Ligne de Commande (Test rapide)
Pour faire une recherche simple directement dans le terminal :
```powershell
python D:\RAG_Knowledge\Scripts\RAG_Engine\rag_engine.py
# Entrez votre recherche quand demandé (ex: "SQL injection wordpress")
```

### 2. Mode API Serveur (Recommandé pour intégration)
Pour lancer le serveur et le rendre accessible à d'autres outils (Gemini, Scripts, VSCode...) :
```powershell
python D:\RAG_Knowledge\Scripts\RAG_Engine\rag_api.py
```
Le serveur écoutera sur `http://localhost:8000`.

### 📚 Documentation de l'API (Swagger UI)
Une fois le serveur lancé, ouvrez votre navigateur sur :
`http://localhost:8000/docs`
Vous aurez une interface graphique pour tester les requêtes API manuellement.

## 🔌 Intégration avec d'autres IA
C'est ici que la magie opère. Vous pouvez connecter ce RAG à n'importe quel LLM capable de faire des appels HTTP (Function Calling) ou via un script intermédiaire.

**Exemple de requête (CURL) :**
```bash
curl -X POST "http://localhost:8000/search" -H "Content-Type: application/json" -d '{"query": "CVE-2023 wordpress", "category": "pentest"}'
```

**Réponse JSON type :**
```json
{
  "stackoverflow": [...],
  "documentation": [
    {
       "source": "Docs",
       "file": "wordpress_exploits.md",
       "excerpt": "...detailed analysis of CVE-2023-xyz..."
    }
  ]
}
```
