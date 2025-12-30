#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Téléchargement ressources complémentaires pour RAG (Mode D:)
Frontend (MDN), DevOps, PHP, Node, etc.
"""

import subprocess
import os
import sys
from pathlib import Path

# Force encoding utf-8 for Windows consoles
sys.stdout.reconfigure(encoding='utf-8')

class ComplementaryDocsDownloader:
    
    REPOSITORIES = {
        "frontend": {
            "mdn-content": "https://github.com/mdn/content.git",
            "devdocs": "https://github.com/freeCodeCamp/devdocs.git",
        },
        "devops": {
            "docker-docs": "https://github.com/docker/docs.git",
            "kubernetes-docs": "https://github.com/kubernetes/website.git",
            "helm": "https://github.com/helm/helm.git",
            "terraform-docs": "https://github.com/hashicorp/terraform.git",
        },
        "ecommerce": {
            "woocommerce-core": "https://github.com/woocommerce/woocommerce.git",
            "stripe-php": "https://github.com/stripe/stripe-php.git",
        },
        "web-servers": {
            "nginx": "https://github.com/nginx/nginx.git",
            "apache-httpd": "https://github.com/apache/httpd.git",
        },
        "caching": {
            "redis-doc": "https://github.com/redis/redis-doc.git",
            "varnish-cache": "https://github.com/varnishcache/varnish-cache.git",
        },
        "git": {
            "git-docs": "https://github.com/git/git.git",
            "github-docs": "https://github.com/github/docs.git",
        },
        "apis": {
            "openapi-spec": "https://github.com/OAI/OpenAPI-Specification.git",
            "graphql-spec": "https://github.com/graphql/graphql-spec.git",
            "rest-api-guidelines": "https://github.com/microsoft/api-guidelines.git",
        },
        "monitoring": {
            "prometheus-docs": "https://github.com/prometheus/docs.git",
            "grafana": "https://github.com/grafana/grafana.git",
        },
        "php": {
            "php-src": "https://github.com/php/php-src.git",
            "laravel-docs": "https://github.com/laravel/docs.git",
            "symfony-docs": "https://github.com/symfony/symfony-docs.git",
            "composer": "https://github.com/composer/composer.git",
        },
        "nodejs": {
            "nodejs-docs": "https://github.com/nodejs/node.git",
            "express": "https://github.com/expressjs/expressjs.com.git",
        },
        "css-frameworks": {
            "bootstrap": "https://github.com/twbs/bootstrap.git",
            "tailwindcss": "https://github.com/tailwindlabs/tailwindcss.git",
        },
        "accessibility": {
            "wcag": "https://github.com/w3c/wcag.git",
            "aria-practices": "https://github.com/w3c/aria-practices.git",
        },
    }
    
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.raw_path = self.base_path / "raw"
        self.raw_path.mkdir(parents=True, exist_ok=True)
    
    def clone_repository(self, category: str, name: str, url: str):
        """Clone un dépôt avec sparse-checkout pour docs seulement"""
        
        target_dir = self.raw_path / category / name
        
        if target_dir.exists():
            print(f"   ⊘ {name} déjà présent")
            return
        
        print(f"   ⬇️  Clonage: {name}...")
        
        
        # Exception pour WooCommerce: Clone complet car doc éparpillée
        if "woocommerce" in name:
            try:
                print(f"   ⬇️  Clonage COMPLET (WooCommerce): {name}...")
                subprocess.run(["git", "clone", "--depth", "1", url, str(target_dir)], check=True, capture_output=True)
                print(f"   ✓ {name} cloné (Full Repo)")
                return
            except Exception as e:
                print(f"   ✗ Erreur Woo: {e}")
                return

        try:
            # Clone avec sparse filter
            subprocess.run([
                "git", "clone",
                "--depth", "1",
                "--filter=blob:none",
                "--sparse",
                url,
                str(target_dir)
            ], check=True, capture_output=True)
            
            # Sparse checkout intelligemment large mais sans erreur
            os.chdir(target_dir)
            try:
                subprocess.run([
                    "git", "sparse-checkout", "set",
                    "docs", "doc", "documentation", "content", "website", "README*", "*.md"
                ], capture_output=True, check=True)
            except:
                pass # Continue même si sparse échoue (on aura le repo partiel)
            
            os.chdir(self.base_path)
            
            print(f"   ✓ {name} cloné")
        except Exception as e:
            print(f"   ✗ Erreur: {e}")
    
    def download_all(self):
        """Télécharge toutes les ressources"""
        
        print("="*70)
        print("📚 TÉLÉCHARGEMENT RESSOURCES COMPLÉMENTAIRES (Mode D:)")
        print("="*70 + "\n")
        
        for category, repos in self.REPOSITORIES.items():
            print(f"\n📂 {category.upper()}")
            print("─"*70)
            
            for name, url in repos.items():
                self.clone_repository(category, name, url)
        
        print("\n" + "="*70)
        print("✅ TÉLÉCHARGEMENT TERMINÉ")
        print("="*70 + "\n")

if __name__ == "__main__":
    base_path = "D:/RAG_Knowledge/Docs/Extra"
    print(f"📍 Destination: {base_path}")
    downloader = ComplementaryDocsDownloader(base_path)
    downloader.download_all()
