#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Création d'index sur la base Stack Overflow - Version Robuste
Optimise les recherches pour le RAG avec gestion avancée des erreurs
"""

import sqlite3
import sys
import time
import os

DB_PATH = r"D:\RAG_Knowledge\StackOverflow\so.db"

def create_indexes():
    print("="*70)
    print("🔍 CRÉATION DES INDEX SQL - STACK OVERFLOW (v2 Robuste)")
    print("="*70 + "\n")
    
    # Vérifier que le fichier existe
    if not os.path.exists(DB_PATH):
        print(f"❌ Erreur : Base de données introuvable : {DB_PATH}")
        return
    
    size_gb = os.path.getsize(DB_PATH) / (1024**3)
    print(f"📂 Base de données : {DB_PATH}")
    print(f"📊 Taille : {size_gb:.1f} GB\n")
    
    try:
        print("🔌 Connexion à la base (peut prendre 1-2 minutes sur USB)...")
        start_conn = time.time()
        
        # Connexion avec timeout
        conn = sqlite3.connect(DB_PATH, timeout=300.0)
        conn.execute("PRAGMA journal_mode=WAL")  # Write-Ahead Logging pour performance
        conn.execute("PRAGMA synchronous=NORMAL")  # Moins strict pour vitesse
        cursor = conn.cursor()
        
        elapsed_conn = time.time() - start_conn
        print(f"✓ Connecté en {elapsed_conn:.1f}s\n")
        
        # Vérifier la table
        print("🔍 Vérification de la table posts...")
        cursor.execute("SELECT COUNT(*) FROM posts")
        count = cursor.fetchone()[0]
        print(f"✓ {count:,} posts trouvés\n")
        
        # Vérifier les index existants
        print("📋 Vérification des index existants...")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='posts'")
        existing = [row[0] for row in cursor.fetchall()]
        print(f"   Index actuels : {len(existing)}")
        for idx in existing:
            print(f"   - {idx}")
        print()
        
        # Index 1 : PostTypeId
        if 'idx_posts_type' not in existing:
            print("1️⃣ Création index sur PostTypeId...")
            start = time.time()
            cursor.execute("CREATE INDEX idx_posts_type ON posts(PostTypeId)")
            conn.commit()
            print(f"   ✓ Terminé en {time.time()-start:.1f}s\n")
        else:
            print("1️⃣ Index PostTypeId déjà existant ✓\n")
        
        # Index 2 : ParentId
        if 'idx_posts_parent' not in existing:
            print("2️⃣ Création index sur ParentId...")
            start = time.time()
            cursor.execute("CREATE INDEX idx_posts_parent ON posts(ParentId)")
            conn.commit()
            print(f"   ✓ Terminé en {time.time()-start:.1f}s\n")
        else:
            print("2️⃣ Index ParentId déjà existant ✓\n")
        
        # Index 3 : Score
        if 'idx_posts_score' not in existing:
            print("3️⃣ Création index sur Score...")
            start = time.time()
            cursor.execute("CREATE INDEX idx_posts_score ON posts(Score DESC)")
            conn.commit()
            print(f"   ✓ Terminé en {time.time()-start:.1f}s\n")
        else:
            print("3️⃣ Index Score déjà existant ✓\n")
        
        # Index 4 : Title (simple, pas FTS pour éviter les problèmes)
        if 'idx_posts_title' not in existing:
            print("4️⃣ Création index sur Title...")
            print("   ⚠️  Peut prendre 5-10 minutes...")
            start = time.time()
            cursor.execute("CREATE INDEX idx_posts_title ON posts(Title)")
            conn.commit()
            print(f"   ✓ Terminé en {(time.time()-start)/60:.1f} minutes\n")
        else:
            print("4️⃣ Index Title déjà existant ✓\n")
        
        conn.close()
        
        print("="*70)
        print("✅ INDEXATION TERMINÉE")
        print("="*70)
        print("🚀 Les recherches seront maintenant beaucoup plus rapides !")
        print("\n💡 Note : Pour des recherches Full-Text encore plus rapides,")
        print("   installez l'extension FTS5 de SQLite séparément.\n")
        
    except sqlite3.OperationalError as e:
        print(f"\n❌ Erreur SQLite : {e}")
        print("\n💡 Solutions possibles :")
        print("   1. Fermez tous les programmes qui utilisent so.db")
        print("   2. Vérifiez que le disque D: n'est pas en lecture seule")
        print("   3. Essayez de redémarrer votre PC\n")
    except Exception as e:
        print(f"\n❌ Erreur : {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    create_indexes()
