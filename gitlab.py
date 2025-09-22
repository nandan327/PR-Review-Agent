import requests

class GitLabPR:
    def __init__(self, project_id, token, base_url="https://gitlab.com/api/v4"):
        self.project_id = project_id
        self.token = token
        self.base_url = base_url
        self.headers = {"PRIVATE-TOKEN": token}

    def fetch_prs(self, state="opened"):
        url = f"{self.base_url}/projects/{self.project_id}/merge_requests"
        response = requests.get(url, headers=self.headers, params={"state": state})
        response.raise_for_status()
        return response.json()

    def fetch_pr_files(self, mr_iid):
        url = f"{self.base_url}/projects/{self.project_id}/merge_requests/{mr_iid}/changes"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        changes = response.json()
        return changes["changes"] if "changes" in changes else []

    def get_file_content(self, file_url):
        response = requests.get(file_url, headers=self.headers)
        response.raise_for_status()
        return response.text
