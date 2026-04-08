import httpx
import json

GITHUB_TOKEN = "ADD_GITHUB_TOKEN"
LLM_API_KEY = "ADD_OPENAI_KEY"

async def get_repo_tree(owner, repo, sha):
    url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{sha}?recursive=1"
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers=headers)
    return r.json()

def filter_paths(tree):
    return [
        f["path"]
        for f in tree.get("tree", [])
        if not any(x in f["path"] for x in ["docs/", "tests/", ".md"])
    ]

async def get_file(owner, repo, path):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers=headers)
    return r.json().get("content","")

def fake_llm_select(issue, paths):
    return paths[:2]

def fake_llm_fix(code):
    return code.replace("password=", "password=os.getenv('PASSWORD')")

async def create_pr(owner, repo, sha):
    return {"pr": "created"}

async def run_pipeline(data):

    tree = await get_repo_tree(
        data["repo_owner"],
        data["repo_name"],
        data["main_sha"]
    )

    paths = filter_paths(tree)

    important_files = fake_llm_select(
        data["issue_body"],
        paths
    )

    fixes = []

    for path in important_files:

        code = await get_file(
            data["repo_owner"],
            data["repo_name"],
            path
        )

        fixed = fake_llm_fix(code)

        fixes.append({
            "path": path,
            "code": fixed
        })

    await create_pr(
        data["repo_owner"],
        data["repo_name"],
        data["main_sha"]
    )

    return {"done": True}
