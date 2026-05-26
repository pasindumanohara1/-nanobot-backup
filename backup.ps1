# OWL Nanobot Backup Script
# Commits and pushes workspace to GitHub

$workspace = "C:\Users\pasindu\.nanobot\workspace"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

Set-Location $workspace

# Stage all changes
git add -A

# Check if there are changes to commit
$status = git status --porcelain
if ($status) {
    git commit -m "Auto backup - $timestamp"
    # Use gh to push via HTTPS with token
    $token = gh auth token
    git push "https://x-access-token:$token@github.com/pasindumanohara1/-nanobot-backup.git" master 2>&1
    Write-Host "Backup completed at $timestamp"
} else {
    Write-Host "No changes to backup at $timestamp"
}
