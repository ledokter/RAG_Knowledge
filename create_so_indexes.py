#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Création d'index sur la base Stack Overflow existante
Optimise les recherches pour le RAG
"""

import sqlite3
import sys
import time

DB_PATH = r"D:\RAG_Knowledge\StackOverflow\so.db"

def create_indexes():
    print("="*70)
    print("🔍 CRÉATION DES INDEX SQL - STACK OVERFLOW")
    print("="*70 + "\n")
    
    print(f"📂 Base de données : {DB_PATH}\n")
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Vérifier que la table existe
        cursor.execute("SELECT COUNT(*) FROM posts")
        count = cursor.fetchone()[0]
        print(f"✓ Base chargée : {count:,} posts trouvés\n")
        
        # Index 1 : PostTypeId (Questions vs Réponses)
        print("1️⃣ Création index sur PostTypeId...")
        start = time.time()
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_posts_type ON posts(PostTypeId)")
        conn.commit()
        elapsed = time.time() - start
        print(f"   ✓ Terminé en {elapsed:.1f}s\n")
        
        # Index 2 : ParentId (Lien Questions-Réponses)
        print("2️⃣ Création index sur ParentId...")
        start = time.time()
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_posts_parent ON posts(ParentId)")
        conn.commit()
        elapsed = time.time() - start
        print(f"   ✓ Terminé en {elapsed:.1f}s\n")
        
        # Index 3 : Score (Tri par popularité)
        print("3️⃣ Création index sur Score...")
        start = time.time()
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_posts_score ON posts(Score DESC)")
        conn.commit()
        elapsed = time.time() - start
        print(f"   ✓ Terminé en {elapsed:.1f}s\n")
        
        # Index 4 : Full-Text Search sur Title (le plus important pour RAG)
        print("4️⃣ Création index Full-Text sur Title...")
        print("   ⚠️  Ceci peut prendre 10-20 minutes...")
        start = time.time()
        
        # Créer une table FTS virtuelle
        cursor.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS posts_fts 
            USING fts5(Id, Title, Body, content='posts', content_rowid='Id')
        """)
        
        # Peupler l'index FTS
        cursor.execute("""
            INSERT INTO posts_fts(posts_fts, rowid, Title, Body)
            SELECT 'delete', Id, Title, Body FROM posts
        """)
        cursor.execute("""
            INSERT INTO posts_fts(rowid, Title, Body)
            SELECT Id, Title, Body FROM posts WHERE PostTypeId = 1
        """)
        
        conn.commit()
        elapsed = time.time() - start
        print(f"   ✓ Terminé en {elapsed/60:.1f} minutes\n")
        
        # Optimiser la base
        print("5️⃣ Optimisation finale (VACUUM)...")
        print("   ⚠️  Peut prendre du temps...")
        start = time.time()
        cursor.execute("VACUUM")
        elapsed = time.time() - start
        print(f"   ✓ Terminé en {elapsed:.1f}s\n")
        
        conn.close()
        
        print("="*70)
        print("✅ INDEXATION TERMINÉE")
        print("="*70)
        print("🚀 Les recherches seront maintenant 100x plus rapides !\n")
        
    except Exception as e:
        print(f"\n❌ Erreur : {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    create_indexes()
