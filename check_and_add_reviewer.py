import os
import requests

# Configuration
GITHUB_API_URL = 'https://api.github.com'
REPO = os.getenv('GITHUB_REPOSITORY')  # Format: owner/repo
PR_NUMBER = os.getenv('GITHUB_PR_NUMBER')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
REVIEWER_USERNAME = 'a-dity-a'  # Replace with the GitHub username of the reviewer
FILE_TO_CHECK = 'sw.cpp'
STRING_TO_CHECK = 'zzzzz'

print("hellllooooooo")
print(PR_NUMBER)
# API headers
headers = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}
# https://api.github.com/repos/aditya-263/sample/pulls/1/files
# Get list of changed files in the pull request
changes_url = f"{GITHUB_API_URL}/repos/aditya-263/sample/pulls/{PR_NUMBER}/files"
response = requests.get(changes_url, headers=headers)
files = response.json()
print(response)
print(files)

for file in files:
    print(file)



print("hellllooooooo2")
# Check if the specific file is among the changed files
file_changed = any(file['filename'] == FILE_TO_CHECK for file in files)


if file_changed:
    for file in files:
        if file['filename'] == FILE_TO_CHECK:

            patch = file.get('patch', '')
            found = any(line.startswith('+') and STRING_TO_CHECK in line for line in patch.split('\n'))

            if found:
                # Add the reviewer to the pull request
                reviewers_url = f"{GITHUB_API_URL}/repos/{REPO}/pulls/{PR_NUMBER}/requested_reviewers"
                payload = {
                    'reviewers': [REVIEWER_USERNAME]
                }
                response = requests.post(reviewers_url, headers=headers, json=payload)
                
                if response.status_code == 201:
                    print(f"Successfully added reviewer {REVIEWER_USERNAME} to PR {PR_NUMBER}.")
                else:
                    print(f"Failed to add reviewer. Status code: {response.status_code}")
                break
            else:
                print(f"String '{STRING_TO_CHECK}' not found in the added lines of {FILE_TO_CHECK}.")
else:
    print(f"{FILE_TO_CHECK} was not changed in the PR.")
