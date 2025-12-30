#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Téléchargement documentation SEO complète pour RAG
ADAPTÉ POUR DISQUE D:
Google SEO, Search Console, Analytics, Bing, Yoast, Schema.org, etc.
"""

import os
import subprocess
import requests
from pathlib import Path
import shutil
import json
import time
import re
import sys

# Force encoding utf-8 for Windows consoles
sys.stdout.reconfigure(encoding='utf-8')

class SEODocsDownloader:
    """Télécharge la documentation SEO complète"""
    
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.raw_path = self.base_path / "raw"
        self.cleaned_path = self.base_path / "cleaned"
        
        self.raw_path.mkdir(parents=True, exist_ok=True)
        self.cleaned_path.mkdir(parents=True, exist_ok=True)
        
        print("="*70)
        print("🔍 TÉLÉCHARGEMENT DOCUMENTATION SEO COMPLÈTE (Mode D:)")
        print("="*70 + "\n")
    
    def download_google_seo_docs(self):
        """Télécharge la documentation Google SEO officielle"""
        print("\n" + "─"*70)
        print("🔵 GOOGLE SEO")
        print("─"*70 + "\n")
        
        google_dir = self.raw_path / "google-seo"
        google_dir.mkdir(exist_ok=True)
        
        # 1. Google Search Central documentation
        print("1️⃣ Google Search Central docs...")
        search_central = google_dir / "search-central"
        if not search_central.exists():
            try:
                subprocess.run(["git", "clone", "--depth", "1", "https://github.com/google-search/search-central.git", str(search_central)], check=True)
                print("   ✓ Search Central clonée\n")
            except: print("   ⚠ Erreur clone\n")
        else: print("   ⊘ Déjà présente\n")
        
        # 3. Quality Rater Guidelines
        print("3️⃣ Quality Rater Guidelines PDF...")
        qrg_url = "https://static.googleusercontent.com/media/guidelines.raterhub.com/en//searchqualityevaluatorguidelines.pdf"
        qrg_file = google_dir / "google-quality-rater-guidelines.pdf"
        if not qrg_file.exists():
            try:
                r = requests.get(qrg_url, timeout=60, stream=True)
                if r.status_code == 200:
                    with open(qrg_file, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192): f.write(chunk)
                    print(f"   ✓ Téléchargé\n")
                else: print("   ⚠ PDF introuvable\n")
            except Exception as e: print(f"   ⚠ Erreur: {e}\n")
        else: print("   ⊘ Déjà présent\n")
    
    def download_schema_org(self):
        print("\n" + "─"*70)
        print("🏷️  SCHEMA.ORG")
        print("─"*70 + "\n")
        schema_dir = self.raw_path / "schema-org"
        schema_dir.mkdir(exist_ok=True)
        schema_repo = schema_dir / "schemaorg"
        if not schema_repo.exists():
            try:
                subprocess.run(["git", "clone", "--depth", "1", "https://github.com/schemaorg/schemaorg.git", str(schema_repo)], check=True)
                print("   ✓ Schema.org cloné\n")
            except: print("   ⚠ Erreur clone\n")
        else: print("   ⊘ Déjà présent\n")
    
    def download_yoast_seo_docs(self):
        print("\n" + "─"*70)
        print("🟢 YOAST SEO")
        print("─"*70 + "\n")
        yoast_dir = self.raw_path / "yoast-seo"
        yoast_dir.mkdir(exist_ok=True)
        
        # Plugin
        yoast_plugin = yoast_dir / "wordpress-seo"
        if not yoast_plugin.exists():
            try:
                subprocess.run(["git", "clone", "--depth", "1", "--filter=blob:none", "--sparse", "https://github.com/Yoast/wordpress-seo.git", str(yoast_plugin)], check=True)
                os.chdir(yoast_plugin)
                subprocess.run(["git", "sparse-checkout", "set", "docs", "README*"], check=True)
                os.chdir(self.base_path)
                print("   ✓ Yoast docs clonées\n")
            except: print("   ⚠ Erreur clone\n")
        else: print("   ⊘ Déjà présent\n")
        
        # Dev docs
        yoast_dev = yoast_dir / "developer-docs"
        if not yoast_dev.exists():
            try:
                subprocess.run(["git", "clone", "--depth", "1", "https://github.com/Yoast/developer-docs.git", str(yoast_dev)], check=True)
                print("   ✓ Dev docs clonées\n")
            except: print("   ⚠ Erreur clone\n")
        else: print("   ⊘ Déjà présent\n")

    def download_structured_data_docs(self):
        print("\n" + "─"*70)
        print("🏗️  STRUCTURED DATA")
        print("─"*70 + "\n")
        structured_dir = self.raw_path / "structured-data"
        structured_dir.mkdir(exist_ok=True)
        
        # JSON-LD
        jsonld = structured_dir / "json-ld"
        if not jsonld.exists():
            try:
                subprocess.run(["git", "clone", "--depth", "1", "https://github.com/json-ld/json-ld.org.git", str(jsonld)], check=True)
                print("   ✓ JSON-LD docs clonées\n")
            except: print("   ⚠ Erreur clone\n")
        else: print("   ⊘ Déjà présent\n")

    def download_wordpress_seo_plugins(self):
        print("\n" + "─"*70)
        print("🔌 WP SEO PLUGINS")
        print("─"*70 + "\n")
        plugins_dir = self.raw_path / "wordpress-seo-plugins"
        plugins_dir.mkdir(exist_ok=True)
        
        seo_plugins = {
            "Rank Math": "https://github.com/rankmath/seo-by-rank-math.git",
            "All in One SEO": "https://github.com/awesomemotive/all-in-one-seo-pack.git",
            "SEOPress": "https://github.com/wp-seopress/seopress.git",
        }
        for name, url in seo_plugins.items():
            print(f"📦 {name}...")
            target = plugins_dir / name.lower().replace(" ","-")
            if not target.exists():
                try:
                    subprocess.run(["git", "clone", "--depth", "1", "--filter=blob:none", "--sparse", url, str(target)], check=True)
                    os.chdir(target)
                    subprocess.run(["git", "sparse-checkout", "set", "README*", "docs"], check=True)
                    os.chdir(self.base_path)
                    print(f"   ✓ {name} cloné\n")
                except: print(f"   ⚠ Erreur {name}\n")
            else: print("   ⊘ Déjà présent\n")

    def download_core_web_vitals_docs(self):
        print("\n" + "─"*70)
        print("⚡ CORE WEB VITALS")
        print("─"*70 + "\n")
        vitals_dir = self.raw_path / "core-web-vitals"
        vitals_dir.mkdir(exist_ok=True)
        
        web_vitals = vitals_dir / "web-vitals"
        if not web_vitals.exists():
            try:
                subprocess.run(["git", "clone", "--depth", "1", "https://github.com/GoogleChrome/web-vitals.git", str(web_vitals)], check=True)
                print("   ✓ Web Vitals cloné\n")
            except: print("   ⚠ Erreur clone\n")
        else: print("   ⊘ Déjà présent\n")

    def extract_and_clean(self):
        print("\n" + "─"*70)
        print("📄 EXTRACTION ET NETTOYAGE")
        print("─"*70 + "\n")
        
        doc_extensions = ['.md', '.txt', '.rst', '.html', '.pdf']
        exclude_dirs = ['.git', 'node_modules', 'vendor', '__pycache__', '.github']
        
        for category_dir in self.raw_path.iterdir():
            if not category_dir.is_dir() or category_dir.name.startswith('.'): continue
            
            print(f"📂 Traitement: {category_dir.name}")
            for file_path in category_dir.rglob("*"):
                if any(excl in file_path.parts for excl in exclude_dirs): continue
                if file_path.suffix.lower() not in doc_extensions: continue
                if not file_path.is_file(): continue
                
                try:
                    rel_path = file_path.relative_to(category_dir)
                    target = self.cleaned_path / category_dir.name / rel_path
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(file_path, target)
                except: pass
            print("   ✓ OK")

    def run(self):
        try:
            self.download_google_seo_docs()
            self.download_schema_org()
            self.download_yoast_seo_docs()
            self.download_structured_data_docs()
            self.download_wordpress_seo_plugins()
            self.download_core_web_vitals_docs()
            self.extract_and_clean()
            
            print("\n" + "="*70)
            print("✅ TERMINÉ")
            print("="*70)
            print(f"📂 Destination: {self.base_path}")
            
        except KeyboardInterrupt: print("\n⚠️ Interrompu.")
        except Exception as e: print(f"\n❌ Erreur: {e}")

if __name__ == "__main__":
    base_path = "D:/RAG_Knowledge/Docs/SEO"
    print(f"📍 Destination: {base_path}")
    downloader = SEODocsDownloader(base_path)
    downloader.run()
