#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MAÎTRE SCRIPT RAG MANAGER
Permet de lancer et mettre à jour tous les modules de la knowledge base.
"""

import os
import sys
import subprocess
import time
from pathlib import Path

# Force encoding
sys.stdout.reconfigure(encoding='utf-8')

SCRIPTS_DIR = Path(__file__).parent
BASE_DRIVE = r"D:\RAG_Knowledge"

SCRIPTS = {
    "1": {
        "name": "WordPress Documentation",
        "file": "wp_downloader.py",
        "desc": "Télécharge Core, Handbooks, Themes & Plugins docs."
    },
    "2": {
        "name": "Bases de Données (SQL)",
        "file": "db_downloader.py",
        "desc": "MySQL, MariaDB, PostgreSQL, phpMyAdmin (PDF & Git)."
    },
    "3": {
        "name": "Pentest & Sécurité",
        "file": "pentest_downloader.py",
        "desc": "Kali, ExploitDB, OWASP, CVE, Nmap, Metasploit."
    },
    "4": {
        "name": "Google Dorks (GHDB)",
        "file": "dorks_downloader.py",
        "desc": "Base de données Google Hacking & Dorks catégorisés."
    },
    "5": {
        "name": "SEO & Search",
        "file": "seo_downloader.py",
        "desc": "Google Search, Schema.org, Yoast, Core Web Vitals."
    },
    "6": {
        "name": "Extra Dev (MDN, DevOps...)",
        "file": "extra_downloader.py",
        "desc": "MDN, Docker, K8s, Laravel, React, Node, Nginx..."
    },
    "7": {
        "name": "Stack Overflow (Indexation)",
        "file": "so_indexer.py",
        "desc": "Convertit le dump 7z en base SQLite (Long & Lourd !)."
    },
    "8": {
        "name": "Stack Overflow (Téléchargement)",
        "file": "download_so_schedule.ps1",
        "desc": "Script PowerShell BITS (Planification nuit)."
    }
}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    print("="*70)
    print("🧠 RAG KNOWLEDGE BASE MANAGER - DISQUE D:")
    print("="*70)
    print("Ce script vous permet de mettre à jour votre base de connaissances.")
    print("Les scripts téléchargent les dernières versions (git pull/clone).")
    print("-" * 70 + "\n")

def run_script(key):
    script_info = SCRIPTS[key]
    script_path = SCRIPTS_DIR / script_info["file"]
    
    print(f"\n🚀 Lancement de : {script_info['name']}...")
    print(f"📄 Script : {script_info['file']}")
    print("-" * 50)
    
    try:
        if script_info["file"].endswith(".py"):
            subprocess.run(["python", str(script_path)], check=True)
        elif script_info["file"].endswith(".ps1"):
            subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", str(script_path)], check=True)
        
        print(f"\n✅ {script_info['name']} terminé avec succès.")
    except Exception as e:
        print(f"\n❌ Erreur lors de l'exécution : {e}")
    
    input("\nAppuyez sur ENTRÉE pour revenir au menu...")

def main():
    while True:
        clear_screen()
        print_header()
        
        print("OPTIONS DISPONIBLES :")
        for key, info in SCRIPTS.items():
            print(f" [{key}] {info['name']}")
            print(f"     └─ {info['desc']}")
        
        print("\n [A] TOUT METTRE À JOUR (Séquentiel - Très long)")
        print(" [Q] Quitter")
        
        choice = input("\n👉 Votre choix : ").strip().upper()
        
        if choice == 'Q':
            print("Au revoir !")
            break
        
        if choice == 'A':
            print("\n⚠️  Vous allez lancer TOUS les scripts de mise à jour.")
            confirm = input("Confirmer ? (O/N) : ")
            if confirm.lower() == 'o':
                for key in sorted(SCRIPTS.keys()):
                    # On saute Stack Overflow indexer/download en mode auto car trop long/spécifique
                    if key in ['7', '8']: continue
                    run_script(key)
            continue
            
        if choice in SCRIPTS:
            run_script(choice)
        else:
            print("❌ Choix invalide.")
            time.sleep(1)

if __name__ == "__main__":
    main()
