import requests
from rest_framework.response import Response

#GITHUB_TOKEN = "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" #token for user rosendomendoza
#GITHUB_USER = "rosendomendoza"
GITHUB_API_URL = "https://api.github.com"
GITHUB_BASE_URL = "https://github.com"



def validate_github_user(username):
    return requests.get(f"{GITHUB_API_URL}/users/{username}")

def validate_github_repo(username, repo_name):
    return requests.get(f"{GITHUB_API_URL}/repos/{username}/{repo_name}")
   
def validate_username_and_repo_url(username, repo_url):
    try:
        if not username or not repo_url:
            return False, "Both 'username' and 'github_url' are required."
        
        https, _, github_url, username_url, repo_name = repo_url.split("/")
        
        if f"{https}//{github_url}" != GITHUB_BASE_URL:
            return False, "Invalid GitHub URL base."
        
        if username != username_url:
            return False, "Username in repository URL does not match the provided username."
        
        return True, repo_name
    except ValueError:
        return False, "Invalid GitHub repository URL structure."
   
# def validate_github_repo(username, repo_name):
#     if username == GITHUB_USER:
#         headers = {
#             "Authorization": f"Bearer {GITHUB_TOKEN}",
#             "Accept": "application/vnd.github.v3+json",
#         }
#         return requests.get(f"{GITHUB_API_URL}/repos/{username}/{repo_name}", headers=headers)
#     return requests.get(f"{GITHUB_API_URL}/repos/{username}/{repo_name}")
 
