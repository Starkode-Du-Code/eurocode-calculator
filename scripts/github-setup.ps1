# Push initial vers GitHub — contourne le PATH non rechargé après winget
# Usage : depuis eurocode-calculator/
#   .\scripts\github-setup.ps1

$Gh = "C:\Program Files\GitHub CLI\gh.exe"

if (-not (Test-Path $Gh)) {
    Write-Host "GitHub CLI introuvable. Installer avec :" -ForegroundColor Red
    Write-Host "  winget install GitHub.cli"
    exit 1
}

Write-Host "GitHub CLI : $Gh" -ForegroundColor Green

$auth = & $Gh auth status 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "`nConnexion GitHub requise (navigateur ou token)..." -ForegroundColor Yellow
    & $Gh auth login
}

if ($LASTEXITCODE -ne 0) {
    Write-Host "Authentification echouee." -ForegroundColor Red
    exit 1
}

$remote = git remote get-url origin 2>$null
if ($remote) {
    Write-Host "`nRemote existant : $remote" -ForegroundColor Cyan
    git push -u origin main
} else {
    Write-Host "`nCreation du repo public eurocode-calculator..." -ForegroundColor Cyan
    & $Gh repo create eurocode-calculator --public --source=. --remote=origin --push
}

if ($LASTEXITCODE -eq 0) {
    Write-Host "`nOK — Repo GitHub pret." -ForegroundColor Green
    & $Gh repo view --web
}
