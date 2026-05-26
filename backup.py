"""
OWL Nanobot Backup Script
Commits and pushes workspace to GitHub using gh CLI for auth.
"""
import subprocess
import os
from datetime import datetime

WORKSPACE = r"C:\Users\pasindu\.nanobot\workspace"
REPO = "https://github.com/pasindumanohara1/-nanobot-backup.git"

def run(cmd, **kwargs):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, **kwargs)
    return result

def main():
    os.chdir(WORKSPACE)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Get token from gh
    token_result = run("gh auth token")
    if token_result.returncode != 0:
        print("ERROR: gh not authenticated. Run: gh auth login")
        return
    token = token_result.stdout.strip()
    
    # Set remote URL with token
    auth_url = f"https://x-access-token:{token}@github.com/pasindumanohara1/-nanobot-backup.git"
    run(f'git remote set-url origin "{auth_url}"')
    
    # Stage all changes
    run("git add -A")
    
    # Check for changes
    status = run("git status --porcelain")
    if status.stdout.strip():
        # Commit
        commit = run(f'git commit -m "Auto backup - {timestamp}"')
        if commit.returncode != 0:
            print(f"Commit failed: {commit.stderr}")
            return
        
        # Push
        push = run('git push origin master', timeout=120)
        if push.returncode == 0:
            print(f"Backup completed at {timestamp}")
        else:
            print(f"Push failed: {push.stderr}")
    else:
        print(f"No changes to backup at {timestamp}")

if __name__ == "__main__":
    main()
