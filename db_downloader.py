#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Téléchargement documentation bases de données pour RAG
ADAPTÉ POUR DISQUE D:
MySQL, MariaDB, PostgreSQL, phpMyAdmin
"""

import os
import subprocess
import requests
from pathlib import Path
import shutil
import re
import json
import time
import sys

# Force encoding utf-8 for Windows consoles
sys.stdout.reconfigure(encoding='utf-8')

class DatabaseDocsDownloader:
    """Télécharge la documentation des bases de données"""
    
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.raw_path = self.base_path / "raw"
        self.cleaned_path = self.base_path / "cleaned"
        
        self.raw_path.mkdir(parents=True, exist_ok=True)
        self.cleaned_path.mkdir(parents=True, exist_ok=True)
        
        print("="*70)
        print("📚 TÉLÉCHARGEMENT DOCUMENTATION BASES DE DONNÉES (Mode D:)")
        print("="*70 + "\n")
    
    
    def download_mysql_docs(self):
        """Télécharge la documentation MySQL"""
        
        print("\n" + "─"*70)
        print("🐬 MYSQL DOCUMENTATION")
        print("─"*70 + "\n")
        
        mysql_dir = self.raw_path / "mysql"
        mysql_dir.mkdir(exist_ok=True)
        
        # 1. Clone du dépôt GitHub MySQL Server (Backup sparse)
        print("1️⃣ Clone du dépôt MySQL Server...")
        mysql_repo = mysql_dir / "mysql-server"
        
        if not mysql_repo.exists():
            try:
                subprocess.run([
                    "git", "clone", 
                    "--depth", "1",
                    "--filter=blob:none",
                    "--sparse",
                    "https://github.com/mysql/mysql-server.git",
                    str(mysql_repo)
                ], check=True)
                
                os.chdir(mysql_repo)
                subprocess.run(["git", "sparse-checkout", "set", "Docs", "man"], check=True)
                os.chdir(self.base_path)
                print("   ✓ MySQL Server docs clonées\n")
            except subprocess.CalledProcessError as e:
                print(f"   ⚠ Erreur clone: {e}\n")
        else:
            print("   ⊘ MySQL Server déjà présent\n")
        
        # 2. Téléchargement des manuels HTML (Archives TAR.GZ plus fiables)
        print("2️⃣ Téléchargement des manuels MySQL (HTML Archives)...")
        
        manuals_dir = mysql_dir / "manuals"
        manuals_dir.mkdir(exist_ok=True)
        
        mysql_docs = {
            "MySQL 8.4 Manual": "https://downloads.mysql.com/docs/refman-8.4-en.html-chapter.tar.gz",
            "MySQL 8.0 Manual": "https://downloads.mysql.com/docs/refman-8.0-en.html-chapter.tar.gz",
        }
        
        for name, url in mysql_docs.items():
            filename = url.split('/')[-1]
            output_file = manuals_dir / filename
            
            if not output_file.exists():
                print(f"   ⬇️  {name}...")
                try:
                    # Utiliser Requests + Stream
                    headers = {'User-Agent': 'Mozilla/5.0'}
                    r = requests.get(url, stream=True, timeout=120, headers=headers)
                    if r.status_code == 200:
                        with open(output_file, 'wb') as f:
                            for chunk in r.iter_content(chunk_size=8192):
                                f.write(chunk)
                        
                        # Extraction automatique
                        print(f"   🔄 Extraction {filename}...")
                        import tarfile
                        try:
                            with tarfile.open(output_file, 'r:gz') as tar:
                                tar.extractall(path=manuals_dir)
                            print(f"   ✓ OK\n")
                        except:
                            print(f"   ⚠ Erreur extraction TAR\n")
                    else:
                        print(f"   ⚠ HTTP {r.status_code}\n")
                except Exception as e:
                    print(f"   ✗ Erreur: {e}\n")
            else:
                print(f"   ⊘ {name} existe déjà\n")
    
    def download_mariadb_docs(self):
        """Télécharge la documentation MariaDB"""
        print("\n" + "─"*70)
        print("🦭 MARIADB DOCUMENTATION")
        print("─"*70 + "\n")
        
        mariadb_dir = self.raw_path / "mariadb"
        mariadb_dir.mkdir(exist_ok=True)
        
        # 1. Clone MariaDB documentation
        print("1️⃣ Clone MariaDB documentation repository...")
        docs_repo = mariadb_dir / "mariadb-documentation"
        
        if not docs_repo.exists():
            try:
                subprocess.run([
                    "git", "clone", "--depth", "1",
                    "https://github.com/MariaDB/mariadb-documentation.git",
                    str(docs_repo)
                ], check=True)
                print("   ✓ MariaDB documentation clonée\n")
            except:
                print("   ⚠ Erreur clone documentation\n")
        else:
            print("   ⊘ Documentation déjà présente\n")
        
        # 2. Knowledge Base Dataset (Skipped for speed/complexity, relying on git repo above which usually has content)

    def download_postgresql_docs(self):
        """Télécharge la documentation PostgreSQL"""
        print("\n" + "─"*70)
        print("🐘 POSTGRESQL DOCUMENTATION")
        print("─"*70 + "\n")
        
        pg_dir = self.raw_path / "postgresql"
        pg_dir.mkdir(exist_ok=True)
        
        # 1. Clone du dépôt PostgreSQL (Docs only)
        print("1️⃣ Clone du dépôt PostgreSQL (Sparse Docs)...")
        pg_repo = pg_dir / "postgres"
        
        if not pg_repo.exists():
            try:
                subprocess.run([
                    "git", "clone", "--depth", "1", "--filter=blob:none", "--sparse",
                    "https://github.com/postgres/postgres.git", str(pg_repo)
                ], check=True)
                
                os.chdir(pg_repo)
                try:
                    subprocess.run(["git", "sparse-checkout", "set", "doc"], check=True)
                except:
                    pass
                os.chdir(self.base_path)
                print("   ✓ PostgreSQL docs clonées\n")
            except:
                print("   ⚠ Erreur clone PG\n")
        else:
            print("   ⊘ PostgreSQL déjà présent\n")
        
        # 2. PDFs
        print("2️⃣ Téléchargement des manuels PDF PostgreSQL...")
        pg_pdfs = {
            "PostgreSQL 16": "https://www.postgresql.org/files/documentation/pdf/16/postgresql-16-A4.pdf",
        }
        pdf_dir = pg_dir / "manuals"
        pdf_dir.mkdir(exist_ok=True)
        
        for name, url in pg_pdfs.items():
            filename = url.split('/')[-1]
            output_file = pdf_dir / filename
            if not output_file.exists():
                print(f"   ⬇️  {name}...")
                try:
                    r = requests.get(url, stream=True, timeout=60)
                    if r.status_code == 200:
                        with open(output_file, 'wb') as f:
                            for chunk in r.iter_content(chunk_size=8192):
                                f.write(chunk)
                        print(f"   ✓ OK: {filename}\n")
                    else:
                        print(f"   ⚠ HTTP {r.status_code}\n")
                except:
                    print("   ✗ Erreur PDF\n")
            else:
                print(f"   ⊘ {filename} existe déjà\n")

    def download_phpmyadmin_docs(self):
        print("\n" + "─"*70)
        print("🔧 PHPMYADMIN")
        print("─"*70 + "\n")
        pma_dir = self.raw_path / "phpmyadmin"
        pma_dir.mkdir(exist_ok=True)
        
        # Clone docs
        docs_repo = pma_dir / "phpmyadmin-docs"
        if not docs_repo.exists():
            try:
                subprocess.run(["git", "clone", "--depth", "1", "https://github.com/phpmyadmin/phpmyadmin.git", str(docs_repo)], check=True)
                print("   ✓ phpMyAdmin repo cloné\n")
            except:
                print("   ⚠ Erreur clone\n")
        else:
            print("   ⊘ Déjà présent\n")

    def extract_documentation(self):
        """Extrait et nettoie la documentation"""
        print("\n" + "─"*70)
        print("📄 EXTRACTION ET NETTOYAGE VERS 'CLEANED'")
        print("─"*70 + "\n")
        
        doc_extensions = ['.md', '.txt', '.rst', '.html', '.pdf'] # Added pdf copy
        exclude_dirs = ['.git', 'node_modules', 'vendor', 'tests']
        
        for db_name in ["mysql", "mariadb", "postgresql", "phpmyadmin"]:
            source_dir = self.raw_path / db_name
            if not source_dir.exists():
                continue
            
            print(f"📂 Traitement: {db_name}")
            
            for file_path in source_dir.rglob("*"):
                if any(excl in file_path.parts for excl in exclude_dirs):
                    continue
                if file_path.suffix.lower() not in doc_extensions:
                    continue
                if not file_path.is_file():
                    continue
                
                relative_path = file_path.relative_to(source_dir)
                target_path = self.cleaned_path / db_name / relative_path
                
                try:
                    target_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(file_path, target_path)
                except Exception as e:
                    pass # Ignore copy errors for simplicity
            
            print(f"   ✓ Copié vers cleaned/{db_name}")

    def run(self):
        try:
            self.download_mysql_docs()
            self.download_mariadb_docs()
            self.download_postgresql_docs()
            self.download_phpmyadmin_docs()
            self.extract_documentation()
            
            print("\n" + "="*70)
            print("✅ TÉLÉCHARGEMENT TERMINÉ")
            print("="*70)
            print(f"📂 Destination: {self.base_path}")
            
        except KeyboardInterrupt:
            print("\n⚠️ Interrompu.")
        except Exception as e:
            print(f"\n❌ Erreur globale: {e}")

if __name__ == "__main__":
    # Hardcoded path for user context
    base_path = "D:/RAG_Knowledge/Docs/Databases"
    print(f"📍 Destination: {base_path}")
    
    downloader = DatabaseDocsDownloader(base_path)
    downloader.run()
