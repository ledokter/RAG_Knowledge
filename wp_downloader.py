#!/usr/bin/env python3
"""
Téléchargement et préparation documentation WordPress pour RAG
ADAPTÉ POUR DISQUE D:
"""

import os
import subprocess
from pathlib import Path
import re
import shutil
import sys

# Force encoding utf-8 for Windows consoles
sys.stdout.reconfigure(encoding='utf-8')

class WordPressDocDownloader:
    """Télécharge et prépare la doc WordPress"""
    
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.raw_path = self.base_path / "raw"
        self.cleaned_path = self.base_path / "cleaned"
        
        self.raw_path.mkdir(parents=True, exist_ok=True)
        self.cleaned_path.mkdir(parents=True, exist_ok=True)
    
    def clone_repositories(self):
        """Clone tous les dépôts GitHub WordPress"""
        
        repos = {
            "wordpress-develop": "https://github.com/WordPress/wordpress-develop.git",
            "devhub": "https://github.com/WordPress/devhub.git",
            "theme-handbook": "https://github.com/WordPress/theme-handbook.git",
            "plugin-handbook": "https://github.com/WordPress/plugin-handbook.git",
            "rest-api-handbook": "https://github.com/WordPress/rest-api-handbook.git",
            # "gutenberg": "https://github.com/WordPress/gutenberg.git", # Often huge, optional
            "coding-standards": "https://github.com/WordPress/WordPress-Coding-Standards.git",
        }
        
        print("📦 Clonage des dépôts WordPress...\n")
        
        for name, url in repos.items():
            target_dir = self.raw_path / name
            
            if target_dir.exists():
                print(f"⊘ {name} existe déjà, ignoré")
                continue
            
            print(f"⬇️  Clonage: {name}...")
            
            try:
                subprocess.run(
                    ["git", "clone", "--depth", "1", url, str(target_dir)],
                    check=True,
                    capture_output=True
                )
                print(f"✓ {name} cloné\n")
            except subprocess.CalledProcessError as e:
                print(f"✗ Erreur: {e}\n")
            except FileNotFoundError:
                print("✗ Erreur: Git n'est pas installé ou pas dans le PATH.\n")
                return
    
    def extract_documentation(self):
        """Extrait uniquement les fichiers de documentation"""
        
        print("\n📄 Extraction des fichiers documentation...\n")
        
        doc_extensions = ['.md', '.txt', '.rst', '.html']
        exclude_dirs = ['.git', 'node_modules', 'vendor', 'tests']
        
        total_files = 0
        total_size = 0
        
        for source_dir in self.raw_path.iterdir():
            if not source_dir.is_dir():
                continue
            
            print(f"📂 Traitement: {source_dir.name}")
            
            for file_path in source_dir.rglob("*"):
                # Ignorer certains dossiers
                if any(excl in file_path.parts for excl in exclude_dirs):
                    continue
                
                # Garder uniquement les extensions doc
                if file_path.suffix.lower() not in doc_extensions:
                    continue
                
                # Chemins relatifs
                relative_path = file_path.relative_to(source_dir)
                target_path = self.cleaned_path / source_dir.name / relative_path
                
                # Copier le fichier
                try:
                    target_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(file_path, target_path)
                    
                    total_files += 1
                    total_size += file_path.stat().st_size
                except Exception as e:
                    print(f"Skipping {file_path}: {e}")
            
            print(f"   ✓ {source_dir.name} traité")
        
        print(f"\n📊 Total: {total_files} fichiers ({total_size / 1024 / 1024:.2f} MB)")
    
    def clean_markdown_files(self):
        """Nettoie les fichiers Markdown pour le RAG"""
        
        print("\n🧹 Nettoyage des fichiers Markdown...\n")
        
        cleaned_count = 0
        
        for md_file in self.cleaned_path.rglob("*.md"):
            try:
                with open(md_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # Suppression des liens internes GitHub
                content = re.sub(r'\[([^\]]+)\]\(\.\.?/[^\)]+\)', r'\1', content)
                
                # Suppression des images (garde juste l'alt text)
                content = re.sub(r'!\[([^\]]*)\]\([^\)]+\)', r'Image: \1', content)
                
                # Suppression des badges
                content = re.sub(r'\[!\[[^\]]+\]\([^\)]+\)\]\([^\)]+\)', '', content)
                
                # Suppression du HTML
                content = re.sub(r'<[^>]+>', '', content)
                
                # Normalisation des espaces
                content = re.sub(r'\n{3,}', '\n\n', content)
                
                with open(md_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                cleaned_count += 1
                
            except Exception as e:
                print(f"⚠ Erreur sur {md_file.name}: {e}")
        
        print(f"✓ {cleaned_count} fichiers nettoyés")
    
    def run(self):
        """Exécute le téléchargement complet"""
        
        print("="*70)
        print("📚 TÉLÉCHARGEMENT DOCUMENTATION WORDPRESS (Mode D:)")
        print("="*70 + "\n")
        
        self.clone_repositories()
        self.extract_documentation()
        self.clean_markdown_files()
        
        print("\n" + "="*70)
        print("✅ TÉLÉCHARGEMENT TERMINÉ")
        print("="*70)
        print(f"📂 Documentation nettoyée: {self.cleaned_path}")


if __name__ == "__main__":
    # Hardcoded path for user context
    base_path = "D:/RAG_Knowledge/Docs/WordPress"
    
    downloader = WordPressDocDownloader(base_path)
    downloader.run()
