# RAG Knowledge Base - Scripts & Tools

Ce dépôt contient l'ensemble des scripts pour construire et maintenir une base de connaissances RAG (Retrieval-Augmented Generation) massive et multi-domaines.

## 🎯 Objectif

Créer une base de connaissances locale complète couvrant :
- Stack Overflow (60M+ posts)
- Documentation technique (WordPress, Bases de données, DevOps)
- Cybersécurité & Pentest (Kali, OWASP, Exploit-DB)
- SEO & Marketing (Google, Schema.org)
- Développement Web (MDN, Frameworks)

## 📦 Contenu du Dépôt

### Scripts de Téléchargement
- `db_downloader.py` - Documentation bases de données (MySQL, PostgreSQL, MariaDB)
- `wp_downloader.py` - Documentation WordPress complète
- `pentest_downloader.py` - Ressources cybersécurité
- `seo_downloader.py` - Documentation SEO
- `extra_downloader.py` - Ressources complémentaires (MDN, DevOps, etc.)
- `dorks_downloader.py` - Google Hacking Database
- `download_so_schedule.ps1` - Téléchargement Stack Overflow (PowerShell)

### Scripts d'Indexation
- `so_indexer.py` - Conversion dump Stack Overflow vers SQLite
- `create_so_indexes.py` - Création des index SQL pour optimiser les recherches

### Moteur RAG
- `rag_engine.py` - Moteur de recherche hybride
- `rag_api.py` - API REST pour interrogation

### Utilitaires
- `rag_manager.py` - Interface de gestion centralisée
- `audit_folders.ps1` - Audit de l'intégrité des données

## 🚀 Installation

### Prérequis
```bash
# Python 3.8+
pip install requests py7zr beautifulsoup4 fastapi uvicorn

# Git
# PowerShell (Windows)
```

### Configuration
Les scripts sont configurés par défaut pour `D:\RAG_Knowledge`. 
Modifiez les chemins dans chaque script si nécessaire.

## 📖 Utilisation

### Mode Simple (Menu Interactif)
```bash
python rag_manager.py
```

### Mode Avancé (Scripts Individuels)
```bash
# Télécharger la documentation MySQL
python db_downloader.py

# Indexer Stack Overflow
python so_indexer.py

# Optimiser les recherches (créer les index SQL)
python create_so_indexes.py

# Lancer l'API RAG
python rag_api.py
```

## 🏗️ Architecture

```
D:\RAG_Knowledge\
├── StackOverflow\
│   ├── stackoverflow.com-Posts.7z (source)
│   └── so.db (indexé)
├── Docs\
│   ├── Databases\
│   ├── WordPress\
│   ├── Pentest\
│   ├── SEO\
│   └── Extra\
└── Scripts\
    └── RAG_Engine\
```

## ⚙️ Fonctionnalités

- ✅ Téléchargement automatisé avec reprise
- ✅ Sparse checkout Git pour économiser l'espace
- ✅ Extraction et nettoyage automatique
- ✅ Indexation SQLite optimisée
- ✅ API REST pour intégration
- ✅ Support multi-sources

## 📊 Volumes de Données

- Stack Overflow : ~150 GB (compressé 23 GB)
- Documentation : ~20-50 GB
- Total estimé : ~200 GB

## 🔌 Intégration

L'API RAG peut être utilisée avec :
- LLMs locaux (Llama, Mistral)
- Services cloud (GPT-4, Claude, Gemini)
- Outils CLI personnalisés

Exemple d'appel API :
```bash
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "SQL injection prevention", "category": "all"}'
```

## 📝 Notes Importantes

- **Espace disque** : Prévoir minimum 250 GB
- **Temps de téléchargement** : Variable selon connexion (plusieurs heures)
- **Indexation SO** : Peut prendre 2-3 heures
- **Licences** : Respecter les licences des sources (CC-BY-SA pour SO)

## 🛠️ Maintenance

- Relancer les scripts de download pour mettre à jour
- Utiliser `audit_folders.ps1` pour vérifier l'intégrité
- Consulter les logs en cas d'erreur

## 🤝 Contribution

Ce projet est conçu pour être extensible. Pour ajouter une nouvelle source :
1. Créer un nouveau script `*_downloader.py`
2. Suivre le pattern des scripts existants
3. Ajouter au `rag_manager.py`

## 📄 Licence

Les scripts sont fournis "as-is". Les données téléchargées sont soumises à leurs licences respectives.

## 🔗 Ressources

- [Stack Overflow Data Dump](https://archive.org/details/stackexchange)
- [OWASP](https://owasp.org)
- [Exploit-DB](https://www.exploit-db.com)
- [MySQL Documentation](https://dev.mysql.com/doc/)

---

**Auteur** : Projet RAG pro-dig-it.com  
**Version** : 1.0  
**Date** : Décembre 2024
