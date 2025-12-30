#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Téléchargement Google Hacking Database (GHDB) et Google Dorks
Complément pour le RAG pentest/security (Mode D:)
"""

import os
import subprocess
import requests
from pathlib import Path
import json
import time
import re
import sys

# Force encoding utf-8 for Windows consoles
sys.stdout.reconfigure(encoding='utf-8')

class GoogleDorksDownloader:
    """Télécharge la Google Hacking Database et collections de dorks"""
    
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.raw_path = self.base_path / "raw"
        self.cleaned_path = self.base_path / "cleaned"
        
        self.raw_path.mkdir(parents=True, exist_ok=True)
        self.cleaned_path.mkdir(parents=True, exist_ok=True)
        
        print("="*70)
        print("🔎 TÉLÉCHARGEMENT GOOGLE HACKING DATABASE (GHDB) - Mode D:")
        print("="*70 + "\n")
    
    def download_ghdb_from_exploitdb(self):
        """Télécharge la GHDB officielle depuis Exploit-DB"""
        print("\n" + "─"*70)
        print("💥 GHDB (EXPLOIT-DB)")
        print("─"*70 + "\n")
        
        ghdb_dir = self.raw_path / "ghdb-exploitdb"
        ghdb_dir.mkdir(exist_ok=True)
        
        print("1️⃣ Clone Exploit-DB (GHDB)...")
        exploitdb_repo = ghdb_dir / "exploitdb"
        if not exploitdb_repo.exists():
            try:
                subprocess.run(["git", "clone", "--depth", "1", "https://github.com/offensive-security/exploitdb.git", str(exploitdb_repo)], check=True)
                print("   ✓ Exploit-DB cloné\n")
            except: print("   ⚠ Erreur clone\n")
        else: print("   ⊘ Déjà présent\n")
        
        print("2️⃣ Extraction des Dorks...")
        ghdb_csv = exploitdb_repo / "ghdb.csv"
        if ghdb_csv.exists():
            self._parse_ghdb_csv(ghdb_csv, ghdb_dir)
        else:
            print("   ⚠ ghdb.csv introuvable\n")

    def _parse_ghdb_csv(self, csv_path: Path, output_dir: Path):
        import csv
        print(f"   📊 Parsing {csv_path.name}...")
        categories = {}
        all_dorks = []
        try:
            with open(csv_path, 'r', encoding='utf-8', errors='ignore') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    category = row.get('category', 'Unknown')
                    entry = {
                        "id": row.get('id',''),
                        "dork": row.get('dork',''),
                        "description": row.get('description',''),
                        "author": row.get('author',''),
                        "date": row.get('date',''),
                        "category": category
                    }
                    if category not in categories: categories[category] = []
                    categories[category].append(entry)
                    all_dorks.append(entry)
            
            for cat, dorks in categories.items():
                clean_cat = re.sub(r'[^\w\s-]', '', cat).strip().replace(' ', '-')
                with open(output_dir / f"ghdb_{clean_cat}.json", 'w', encoding='utf-8') as f:
                    json.dump(dorks, f, indent=2)
                with open(output_dir / f"ghdb_{clean_cat}.md", 'w', encoding='utf-8') as f:
                    f.write(f"# Dorks - {cat}\n\n")
                    for d in dorks:
                        f.write(f"## {d['description']}\n`{d['dork']}`\n\n")
            
            with open(output_dir / "ghdb_complete.json", 'w', encoding='utf-8') as f:
                json.dump(all_dorks, f, indent=2)
            print(f"   ✓ {len(all_dorks)} Dorks extraits\n")
        except Exception as e: print(f"   ✗ Erreur: {e}\n")

    def download_community_dork_repos(self):
        print("\n" + "─"*70)
        print("🌟 COMMUNAUTÉ")
        print("─"*70 + "\n")
        community_dir = self.raw_path / "community-dorks"
        community_dir.mkdir(exist_ok=True)
        repos = {
            "Awesome-Google-Dorks": "https://github.com/Tobee1406/Awesome-Google-Dorks.git",
            "GHDB-Tools": "https://github.com/RAVIPRAJ/ghdb.git",
            "Google-Dorks-Bug-Bounty": "https://github.com/Proviesec/google-dorks.git",
            "Dorking-Collection": "https://github.com/cipher387/Dorks-collections-list.git",
        }
        for name, url in repos.items():
            print(f"📦 {name}...")
            target = community_dir / name
            if not target.exists():
                try:
                    subprocess.run(["git", "clone", "--depth", "1", url, str(target)], check=True)
                    print(f"   ✓ {name} cloné\n")
                except: print(f"   ⚠ Erreur {name}\n")
            else: print("   ⊘ Déjà présent\n")

    def create_categorized_dorks(self):
        print("\n" + "─"*70)
        print("📂 CRÉATION CATÉGORIES THÉMATIQUES")
        print("─"*70 + "\n")
        categories_dir = self.cleaned_path / "dorks-by-category"
        categories_dir.mkdir(exist_ok=True)
        
        thematic_dorks = {
            "wordpress": {
                "description": "Google Dorks pour WordPress",
                "dorks": ['inurl:wp-content/uploads/', 'inurl:wp-admin intitle:login', 'filetype:sql intext:wp_users']
            },
            "database": {
                "description": "Bases de données exposées",
                "dorks": ['filetype:sql intext:password', 'inurl:database.sql', 'filetype:env intext:DB_PASSWORD']
            },
            "config": {
                "description": "Fichiers config",
                "dorks": ['filetype:conf inurl:proftpd.conf', 'filetype:env DB_PASSWORD']
            },
            "sensitive": {
                "description": "Fichiers sensibles",
                "dorks": ['filetype:log inurl:password', 'filetype:pdf "confidential"']
            }
        }
        
        for name, data in thematic_dorks.items():
            with open(categories_dir / f"{name}_dorks.md", 'w', encoding='utf-8') as f:
                f.write(f"# {name.title()}\n\n{data['description']}\n\n")
                for d in data['dorks']: f.write(f"- `{d}`\n")
        print("   ✓ Catégories créées\n")

    def create_usage_guide(self):
        print("\n" + "─"*70)
        print("📖 CRÉATION GUIDE")
        print("─"*70 + "\n")
        guide_file = self.cleaned_path / "google_dorks_guide.md"
        content = """# Guide Google Dorks
## Opérateurs Basics
- `site:` Domaine spécifique
- `inurl:` Dans l'URL
- `intitle:` Dans le titre
- `filetype:` Type de fichier
"""
        with open(guide_file, 'w', encoding='utf-8') as f: f.write(content)
        print("   ✓ Guide créé\n")

    def run(self):
        try:
            self.download_ghdb_from_exploitdb()
            self.download_community_dork_repos()
            self.create_categorized_dorks()
            self.create_usage_guide()
            print("\n✅ TERMINÉ")
        except KeyboardInterrupt: print("\n⚠️ Interrompu.")
        except Exception as e: print(f"\n❌ Erreur: {e}")

if __name__ == "__main__":
    base_path = "D:/RAG_Knowledge/Docs/Pentest/GoogleDorks"
    print(f"📍 Destination: {base_path}")
    downloader = GoogleDorksDownloader(base_path)
    downloader.run()
