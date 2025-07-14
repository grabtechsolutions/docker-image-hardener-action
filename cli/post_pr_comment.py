import os
import requests

def post_or_update_comment(repo, pr_number, token, comment_body, marker="<!-- DOCKER-HARDENER-START -->"):
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
    }

    # List comments
    comments_url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    response = requests.get(comments_url, headers=headers)
    response.raise_for_status()
    comments = response.json()

    existing_comment_id = None
    for comment in comments:
        if comment.get("body", "").startswith(marker):
            existing_comment_id = comment["id"]
            break

    if existing_comment_id:
        print("✏️ Updating existing PR comment...")
        update_url = f"{comments_url}/{existing_comment_id}"
        requests.patch(update_url, headers=headers, json={"body": comment_body})
    else:
        print("💬 Creating new PR comment...")
        requests.post(comments_url, headers=headers, json={"body": comment_body})

def main():
    repo = os.environ.get("GITHUB_REPOSITORY")
    ref = os.environ.get("GITHUB_REF")
    token = os.environ.get("GITHUB_TOKEN")
    summary_file = os.environ.get("GITHUB_STEP_SUMMARY")

    if not (repo and ref and token and summary_file):
        print("❌ Missing one or more required environment variables.")
        return

    if "refs/pull/" not in ref:
        print("ℹ️ Not a pull request, skipping comment.")
        return

    try:
        pr_number = int(ref.split("/")[2])
    except Exception as e:
        print(f"❌ Failed to extract PR number from ref: {e}")
        return

    try:
        with open(summary_file, "r", encoding="utf-8") as f:
            summary_content = f.read()
    except Exception as e:
        print(f"❌ Failed to read summary file: {e}")
        return

    comment_body = f"""<!-- DOCKER-HARDENER-START -->
## 🐳 Docker Image Scan Results

{summary_content}
"""

    post_or_update_comment(repo, pr_number, token, comment_body)

if __name__ == "__main__":
    main()
