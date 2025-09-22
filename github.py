import requests

class GitHubPR:
    def __init__(self, owner, repo, token):
        self.owner = owner
        self.repo = repo
        self.headers = {"Authorization": f"token {token}"}
        self.api = f"https://api.github.com/repos/{owner}/{repo}/pulls"

    def fetch_prs(self, state="open"):
        response = requests.get(self.api, headers=self.headers, params={"state": state})
        response.raise_for_status()
        return response.json()

    def fetch_pr_files(self, pr_number):
        url = f"https://api.github.com/repos/{self.owner}/{self.repo}/pulls/{pr_number}/files"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_file_content(self, raw_url):
        response = requests.get(raw_url)
        response.raise_for_status()
        return response.text
