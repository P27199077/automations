import requests

# ----------------- CONFIGURATION -----------------
# Paste your GitHub Personal Access Token here
TOKEN = "your gemini api token"

# Your GitHub username
USERNAME = "P27199077"

# List of repository names you want to make PUBLIC
# Example: ["cf-sync-leetfier", "leetcode-sdestriversheet"]
REPOS = [
    "repo namesssss"
]

# -------------------------------------------------

headers = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

print(f"Starting visibility update for {len(REPOS)} repositories...\n")

for repo in REPOS:
    repo = repo.strip()
    url = f"https://api.github.com/repos/{USERNAME}/{repo}"
    
    # Setting private to False changes the visibility to Public
    data = {"private": False}
    
    try:
        response = requests.patch(url, json=data, headers=headers)
        if response.status_code == 200:
            print(f"✓ Success: '{repo}' is now PUBLIC!")
        else:
            err_msg = response.json().get('message', f"HTTP status {response.status_code}")
            print(f"✗ Failed: '{repo}' could not be updated. Reason: {err_msg}")
    except Exception as e:
        print(f"✗ Error updating '{repo}': {str(e)}")

print("\nDone!")
