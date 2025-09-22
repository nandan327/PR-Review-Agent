import requests
from requests.auth import HTTPBasicAuth

class BitbucketPR:
    def __init__(self, workspace, repo_slug, username, app_password):
        self.workspace = workspace
        self.repo_slug = repo_slug
        self.auth = HTTPBasicAuth(username, app_password)
        self.base_url = f"https://api.bitbucket.org/2.0/repositories/{workspace}/{repo_slug}/pullrequests"

    def fetch_prs(self, state="OPEN"):
        response = requests.get(self.base_url, auth=self.auth, params={"state": state})
        response.raise_for_status()
        return response.json().get("values", [])

    def fetch_pr_files(self, pr_id):
        url = f"{self.base_url}/{pr_id}/diffstat"
        response = requests.get(url, auth=self.auth)
        response.raise_for_status()
        return response.json().get("values", [])

    def get_file_content(self, raw_url):
        response = requests.get(raw_url, auth=self.auth)
        response.raise_for_status()
        return response.text
