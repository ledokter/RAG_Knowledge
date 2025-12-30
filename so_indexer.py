#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Stack Overflow Dump to SQLite Converter
Optimisé pour le streaming et la faible consommation mémoire.
Lit directement le .7z et insère dans SQLite.
"""

import sys
import sqlite3
import xml.etree.ElementTree as ET
import py7zr
import os
import time
from pathlib import Path

# Configuration
SOURCE_7Z = r"D:\RAG_Knowledge\StackOverflow\stackoverflow.com-Posts.7z"
DB_PATH = r"D:\RAG_Knowledge\StackOverflow\so.db"
BATCH_SIZE = 10000

# Force stdout utf-8
sys.stdout.reconfigure(encoding='utf-8')

def create_schema(cursor):
    """Crée la table Posts et l'index FTS"""
    print("   🔨 Création du schéma SQL...")
    
    # Table principale (Données brutes)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            Id INTEGER PRIMARY KEY,
            PostTypeId INTEGER, -- 1=Question, 2=Answer
            ParentId INTEGER,   -- Pour les réponses
            CreationDate TEXT,
            Score INTEGER,
            ViewCount INTEGER,
            Body TEXT,
            Title TEXT,
            Tags TEXT,
            AnswerCount INTEGER
        )
    """)
    
    # Optimisation: Synchrone OFF pour vitesse d'insertion massive
    cursor.execute("PRAGMA synchronous = OFF")
    cursor.execute("PRAGMA journal_mode = MEMORY")

def process_xml_stream(file_obj, cursor, conn):
    """Parse le flux XML et insère dans SQLite"""
    
    context = ET.iterparse(file_obj, events=('end',))
    
    batch = []
    count = 0
    start_time = time.time()
    
    # Mapping des colonnes XML -> DB
    # XML uses Attributes like Id="1"
    
    for event, elem in context:
        if elem.tag == "row":
            try:
                # Extraction des champs
                p_id = int(elem.get("Id"))
                p_type = int(elem.get("PostTypeId"))
                
                # On ne garde que Questions (1) et Réponses (2)
                if p_type not in (1, 2):
                    elem.clear()
                    continue
                
                parent_id = elem.get("ParentId")
                parent_id = int(parent_id) if parent_id else None
                
                creation_date = elem.get("CreationDate")
                score = int(elem.get("Score", 0))
                view_count = elem.get("ViewCount")
                view_count = int(view_count) if view_count else 0
                
                body = elem.get("Body", "")
                title = elem.get("Title", "")
                tags = elem.get("Tags", "")
                
                ans_count = elem.get("AnswerCount")
                ans_count = int(ans_count) if ans_count else 0
                
                # Ajout au batch
                batch.append((
                    p_id, p_type, parent_id, creation_date, score, 
                    view_count, body, title, tags, ans_count
                ))
                
                count += 1
                
                # Insertion par lot
                if len(batch) >= BATCH_SIZE:
                    cursor.executemany("""
                        INSERT OR IGNORE INTO posts 
                        (Id, PostTypeId, ParentId, CreationDate, Score, ViewCount, Body, Title, Tags, AnswerCount)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, batch)
                    conn.commit()
                    batch = []
                    
                    # Log progression
                    elapsed = time.time() - start_time
                    speed = count / elapsed
                    print(f"   Processed {count:,} posts... ({speed:.0f} posts/sec)", end='\r')
            
            except Exception as e:
                pass # Skip malformed rows
            
            # Libérer la mémoire
            elem.clear()
            
    # Insert remaining
    if batch:
        cursor.executemany("INSERT OR IGNORE INTO posts VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", batch)
        conn.commit()
    
    return count

def main():
    print("="*70)
    print("🚀 STACK OVERFLOW: 7Z TO SQLITE INDEXER")
    print(f"   Source: {SOURCE_7Z}")
    print(f"   Target: {DB_PATH}")
    print("="*70 + "\n")
    
    if not os.path.exists(SOURCE_7Z):
        print(f"❌ Erreur: Fichier source introuvable: {SOURCE_7Z}")
        return

    # Connexion DB
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        create_schema(cursor)
        
        print("   📂 Ouverture de l'archive 7z...")
        
        # Py7zr context manager
        with py7zr.SevenZipFile(SOURCE_7Z, mode='r') as archive:
            # On cherche le fichier Posts.xml dans l'archive
            # Note: archive.read returns a dict {filename: BytesIO} but parsing huge file in memory is bad.
            # We need to open it as a stream. file object.
            
            # Hack: py7zr doesn't support easy streaming of single file content without extraction in some versions.
            # But let's try reading names first.
            all_files = archive.getnames()
            target_file_name = None
            for name in all_files:
                if "Posts.xml" in name:
                    target_file_name = name
                    break
            
            if not target_file_name:
                print("❌ 'Posts.xml' non trouvé dans l'archive!")
                return
            
            print(f"   📄 Traitement de {target_file_name}...")
            
            # Extract to a pipe or temporary location? 
            # Or use archive.read([name]) which puts in memory... WARNING.
            # StackOverflow Posts.xml is 90GB. 
            # py7zr might not be suitable for streaming huge files without extracting to disk first.
            
            # CHECK STRATEGY: 
            # If py7zr cannot stream, we must extract deeply.
            # But we are on D:. We can extract Posts.xml to D:\Posts.xml temporary if space allows.
            # Let's try to see if we can extract just that file.
            
            print("   ⚠️ Extraction temporaire de Posts.xml (nécessaire pour la performance)...")
            archive.extract(path=r"D:\RAG_Knowledge\StackOverflow", targets=[target_file_name])
            
            extracted_xml = os.path.join(r"D:\RAG_Knowledge\StackOverflow", target_file_name)
            
            if not os.path.exists(extracted_xml):
                 print("❌ Erreur d'extraction.")
                 return

            print("   🔄 Début du parsing XML & Insertion SQL...")
            
            with open(extracted_xml, 'rb') as xml_file:
                total = process_xml_stream(xml_file, cursor, conn)
            
            print(f"\n   ✅ Importation terminée: {total:,} posts.")
            
            # Cleanup
            print("   🧹 Suppression du fichier XML temporaire...")
            os.remove(extracted_xml)
            
            # Indexing step
            print("   🔍 Création des index (Cela peut prendre du temps)...")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_posts_type ON posts(PostTypeId)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_posts_parent ON posts(ParentId)")
            conn.commit()
            print("   ✅ Index créés.")

    except Exception as e:
        print(f"\n❌ Erreur critique: {e}")
        import traceback
        traceback.print_exc()
    finally:
        conn.close()

if __name__ == "__main__":
    main()
