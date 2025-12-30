"""
Moteur de recherche RAG hybride (SQLite + Recherche Fichiers)
Permet d'interroger la base de connaissances D:\RAG_Knowledge
"""

import sqlite3
import os
import re
from pathlib import Path
from typing import List, Dict, Any

# Configuration
BASE_PATH = Path(r"D:\RAG_Knowledge")
DOCS_PATH = BASE_PATH / "Docs"
SO_DB_PATH = BASE_PATH / "StackOverflow" / "so.db"

class KnowledgeBase:
    def __init__(self):
        self.doc_extensions = {'.md', '.txt', '.py', '.json', '.html'}

    def search_stackoverflow(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Recherche dans la base StackOverflow SQLite"""
        results = []
        if not SO_DB_PATH.exists():
            return [{"error": "Base SO non trouvée"}]

        try:
            conn = sqlite3.connect(f"file:{SO_DB_PATH}?mode=ro", uri=True)
            cursor = conn.cursor()
            
            # Recherche basique SQL LIKE (pour l'instant, plus rapide que FTS sans config)
            # On cherche dans le Titre en priorité
            parts = query.split()
            sql_query = "SELECT Id, Title, Body, Score FROM posts WHERE PostTypeId=1"
            params = []
            
            for part in parts:
                sql_query += " AND Title LIKE ?"
                params.append(f"%{part}%")
            
            sql_query += " ORDER BY Score DESC LIMIT ?"
            params.append(limit)
            
            cursor.execute(sql_query, params)
            rows = cursor.fetchall()
            
            for row in rows:
                results.append({
                    "source": "StackOverflow",
                    "id": row[0],
                    "title": row[1],
                    "excerpt": row[2][:500] + "...", # Tronquer le body
                    "score": row[3],
                    "path": f"https://stackoverflow.com/q/{row[0]}"
                })
            
            conn.close()
        except Exception as e:
            results.append({"error": f"Erreur SQL: {e}"})
            
        return results

    def _grep_files(self, query: str, root_dir: Path, limit: int = 5) -> List[Dict[str, Any]]:
        """Recherche textuelle simple dans les fichiers (grep-like)"""
        results = []
        count = 0
        keywords = query.lower().split()
        
        # Parcours récursif (optimisable avec 'grep' système si dispo)
        # Pour Python pur, on limite la profondeur/nombre de fichiers scannés pour la perf
        
        for file_path in root_dir.rglob("*"):
            if count >= limit: break
            if file_path.suffix not in self.doc_extensions: continue
            if "node_modules" in str(file_path): continue
            
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    content_lower = content.lower()
                    
                    # Vérifier si tous les mots clés sont présents
                    if all(k in content_lower for k in keywords):
                        # Trouver l'extrait
                        idx = content_lower.find(keywords[0])
                        start = max(0, idx - 100)
                        end = min(len(content), idx + 400)
                        excerpt = content[start:end].replace('\n', ' ')
                        
                        results.append({
                            "source": "Docs",
                            "file": file_path.name,
                            "path": str(file_path),
                            "excerpt": f"...{excerpt}..."
                        })
                        count += 1
            except:
                pass
                
        return results

    def search_docs_by_category(self, query: str, category: str = "all", limit: int = 5):
        """Recherche dans les fichiers de documentation"""
        if category == "all":
            target_dir = DOCS_PATH
        else:
            # Mapping catégorie -> dossier
            cat_map = {
                "wordpress": "WordPress",
                "sql": "Databases",
                "pentest": "Pentest",
                "seo": "SEO",
                "extra": "Extra"
            }
            target_dir = DOCS_PATH / cat_map.get(category, ".")
            
        if not target_dir.exists():
            return [{"error": f"Catégorie {category} introuvable"}]
            
        return self._grep_files(query, target_dir, limit)

    def unified_search(self, query: str) -> Dict[str, Any]:
        """Recherche agrégée"""
        return {
            "stackoverflow": self.search_stackoverflow(query, limit=3),
            "documentation": self.search_docs_by_category(query, limit=3)
        }

if __name__ == "__main__":
    # Test CLI simple
    kb = KnowledgeBase()
    q = input("🔍 Recherche RAG : ")
    res = kb.unified_search(q)
    
    print("\n--- Stack Overflow ---")
    for r in res['stackoverflow']:
        if 'title' in r: print(f"[{r['score']}] {r['title']} ({r['path']})")
        
    print("\n--- Documentation ---")
    for r in res['documentation']:
        if 'file' in r: print(f"📄 {r['file']}\n   {r['excerpt']}\n")
