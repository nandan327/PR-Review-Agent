from servers.github import GitHubPR
from servers.gitlab import GitLabPR
from servers.bitbucket import BitbucketPR
from analyzer.code_quality import analyze_python_file
from analyzer.ai_suggestions import ai_suggest
import requests

# ------------------ Configuration ------------------
# GitHub
GITHUB_TOKEN = "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"
GITHUB_OWNER = "TUSHAR91316"
GITHUB_REPO = "AI-BASED-NIDS"

# GitLab
GITLAB_TOKEN = "YOUR_GITLAB_TOKEN"
GITLAB_PROJECT_ID = "project_id"

# Bitbucket
BITBUCKET_USER = "username"
BITBUCKET_APP_PASSWORD = "app_password"
BITBUCKET_WORKSPACE = "workspace"
BITBUCKET_REPO = "repo_slug"
# ---------------------------------------------------

def process_pr_files(files, get_content_func):
    for file in files:
        raw_url = file.get("raw_url") or file.get("links", {}).get("self", {}).get("href")
        if not raw_url:
            continue
        content = get_content_func(raw_url)
        feedback = analyze_python_file(content)
        ai_feedback = ai_suggest(content)
        print(f"\nFile: {file.get('filename', file.get('new', 'Unknown'))}")
        if feedback:
            print("Static Analysis Feedback:")
            for comment in feedback:
                print(f"- {comment}")
        else:
            print("No static issues found.")
        if ai_feedback:
            print("AI Suggestions:")
            for suggestion in ai_feedback:
                print(f"- {suggestion}")

def main():
    # ------------------ GitHub ------------------
    print("\nFetching PRs from GitHub...")
    github_agent = GitHubPR(GITHUB_OWNER, GITHUB_REPO, GITHUB_TOKEN)
    gh_prs = github_agent.fetch_prs()
    for pr in gh_prs:
        print(f"\nGitHub PR #{pr['number']}: {pr['title']}")
        files = github_agent.fetch_pr_files(pr['number'])
        process_pr_files(files, github_agent.get_file_content)

    # ------------------ GitLab ------------------
    print("\nFetching PRs from GitLab...")
    gitlab_agent = GitLabPR(GITLAB_PROJECT_ID, GITLAB_TOKEN)
    gl_prs = gitlab_agent.fetch_prs()
    for pr in gl_prs:
        print(f"\nGitLab MR !{pr['iid']}: {pr['title']}")
        files = gitlab_agent.fetch_pr_files(pr['iid'])
        process_pr_files(files, gitlab_agent.get_file_content)

    # ------------------ Bitbucket ------------------
    print("\nFetching PRs from Bitbucket...")
    bb_agent = BitbucketPR(BITBUCKET_WORKSPACE, BITBUCKET_REPO, BITBUCKET_USER, BITBUCKET_APP_PASSWORD)
    bb_prs = bb_agent.fetch_prs()
    for pr in bb_prs:
        print(f"\nBitbucket PR #{pr['id']}: {pr['title']}")
        files = bb_agent.fetch_pr_files(pr['id'])
        process_pr_files(files, bb_agent.get_file_content)

if __name__ == "__main__":
    main()
