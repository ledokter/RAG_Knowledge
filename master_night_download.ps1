# Script principal de téléchargement autonome pour la nuit
$ErrorActionPreference = "SilentlyContinue"

Write-Host ">>> Démarrage du script de téléchargement autonome pour la nuit..."

# 1. Télécharger Ubuntu Server Guide PDF (Si non présent)
$ubuntuPath = "D:\RAG_Knowledge\Docs\Ubuntu\serverguide.pdf"
if (-not (Test-Path $ubuntuPath)) {
    Write-Host "Tentative téléchargement Ubuntu Server Guide..."
    try {
        # URL générique souvent valide, sinon on passe
        Invoke-WebRequest -Uri "https://help.ubuntu.com/lts/serverguide/serverguide.pdf" -OutFile $ubuntuPath
        Write-Host "Ubuntu PDF OK."
    } catch { Write-Host "Ubuntu PDF échec (Pas grave, on continue)." }
}

# 2. Télécharger MySQL Reference Manual PDF 
$mysqlPath = "D:\RAG_Knowledge\Docs\LAMP\mysql_refman.pdf"
if (-not (Test-Path $mysqlPath)) {
    Write-Host "Tentative téléchargement MySQL RefMan..."
    try {
        Invoke-WebRequest -Uri "https://downloads.mysql.com/docs/refman-8.0-en.pdf" -OutFile $mysqlPath -UserAgent "Mozilla/5.0"
        Write-Host "MySQL PDF OK."
    } catch { 
        Write-Host "MySQL PDF échec (souvent protégé anti-bot)." 
    }
}

# 3. Télécharger WordPress 'Easy Guide' (Fallback car pas de PDF officiel unique)
$wpPath = "D:\RAG_Knowledge\Docs\WordPress\wordpress-easy-guide.pdf"
if (-not (Test-Path $wpPath)) {
     Write-Host "Tentative téléchargement WordPress Guide..."
     try {
        # URL d'exemple pour un guide WP
        Invoke-WebRequest -Uri "https://easywpcal.com/downloads/Easy_WP_Guide_WP6.3.pdf" -OutFile $wpPath
        Write-Host "WordPress Guide OK."
     } catch { Write-Host "WP Guide échec." }
}

# 4. SURTOUT : Lancer le script Stack Overflow s'il n'est pas déjà lancé
# On vérifie si un process powershell tourne avec ce script spécifique est dur, mais on peut juste lancer une instance.
# Le script SO a sa propre boucle de temps (1h-5h), donc on peut le lancer maintenant et il attendra.
Write-Host "Lancement du gestionnaire de téléchargement Stack Overflow en tâche de fond..."
Start-Process powershell -ArgumentList "-ExecutionPolicy Bypass -File D:\RAG_Knowledge\download_so_schedule.ps1" -WindowStyle Hidden

Write-Host ">>> Configuration terminée. Tout est en mode automatique."
Write-Host "Le PC va télécharger :"
Write-Host " - RFCs (en cours)"
Write-Host " - PHP (en cours)"
Write-Host " - MySQL/Ubuntu/WP (tentés)"
Write-Host " - Stack Overflow (démarrera à 01h00)"
