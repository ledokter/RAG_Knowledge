$root = "D:\RAG_Knowledge\Docs"
Write-Host ">>> Audit des dossiers vides dans $root..."
Write-Host "---------------------------------------------------"

$dirs = Get-ChildItem -Path $root -Recurse -Directory | Where-Object { $_.FullName -notmatch '\\.git' -and $_.FullName -notmatch '__pycache__' }

$emptyCount = 0

foreach ($d in $dirs) {
    try {
        $files = Get-ChildItem -Path $d.FullName -File
        $count = $files.Count
        
        if ($count -eq 0) {
            # On verifie s'il a des sous-dossiers
            $subdirs = Get-ChildItem -Path $d.FullName -Directory
            if ($subdirs.Count -eq 0) {
                Write-Host "VIDE        : $($d.FullName)" -ForegroundColor Red
                $emptyCount++
            }
        }
    }
    catch {
        Write-Host "Erreur acces : $($d.FullName)"
    }
}

Write-Host "---------------------------------------------------"
Write-Host "Termine. $emptyCount dossiers vides trouves."
