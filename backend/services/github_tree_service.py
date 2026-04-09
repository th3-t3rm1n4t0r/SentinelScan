import requests
import logging
from typing import List, Dict, Optional

from app.config import settings


logger = logging.getLogger("sentinel_scan.github")


# =========================
# CONFIG
# =========================

HEADERS = {

    "Authorization": f"Bearer {settings.GITHUB_TOKEN}",

    "Accept": "application/vnd.github+json"

} if settings.GITHUB_TOKEN else {}


SUPPORTED_EXTENSIONS = (

    ".py",
    ".js",
    ".ts",
    ".java",
    ".go",
    ".rb",
    ".php",
    ".env",
    ".yaml",
    ".yml",
    ".json",
    ".ini",
    ".cfg"

)


MAX_FILES = 120

MAX_FILE_SIZE = 200_000   # 200 KB


# =========================
# PARSE OWNER/REPO
# =========================

def parse_repo_url(

    repo_url: str

) -> tuple:

    repo_url = repo_url.strip().rstrip("/")

    parts = repo_url.split("/")

    if len(parts) < 2:

        raise ValueError("Invalid GitHub repo URL")

    return parts[-2], parts[-1]


# =========================
# GET DEFAULT BRANCH
# =========================

def get_default_branch(

    owner: str,

    repo: str

) -> str:

    url = f"{settings.GITHUB_API_BASE}/repos/{owner}/{repo}"

    response = requests.get(

        url,

        headers=HEADERS,

        timeout=20

    )

    if response.status_code != 200:

        raise Exception(

            f"GitHub repo info failed: {response.text}"

        )

    return response.json().get(

        "default_branch",

        settings.GITHUB_DEFAULT_BRANCH

    )


# =========================
# GET REPO FILES
# =========================

def get_repo_tree(

    repo_url: str,

    branch: Optional[str] = None

) -> List[Dict]:

    owner, repo = parse_repo_url(repo_url)

    logger.info(f"Scanning repo: {owner}/{repo}")


    # branch
    branch = branch or get_default_branch(owner, repo)

    logger.info(f"Using branch: {branch}")


    # tree
    tree_url = (

        f"{settings.GITHUB_API_BASE}/repos/"
        f"{owner}/{repo}/git/trees/"
        f"{branch}?recursive=1"

    )


    tree_response = requests.get(

        tree_url,

        headers=HEADERS,

        timeout=30

    )


    if tree_response.status_code != 200:

        raise Exception(

            f"GitHub tree failed: {tree_response.text}"

        )


    tree_data = tree_response.json()


    files = []

    file_count = 0


    # =====================
    # DOWNLOAD FILES
    # =====================

    for item in tree_data.get("tree", []):

        path = item.get("path", "")

        if not path.endswith(SUPPORTED_EXTENSIONS):

            continue


        if file_count >= MAX_FILES:

            logger.warning("file limit reached")

            break


        raw_url = (

            f"https://raw.githubusercontent.com/"
            f"{owner}/{repo}/"
            f"{branch}/{path}"

        )


        try:

            file_response = requests.get(

                raw_url,

                headers=HEADERS,

                timeout=20

            )


            if file_response.status_code != 200:

                continue


            code = file_response.text


            # skip huge files
            if len(code) > MAX_FILE_SIZE:

                continue


            files.append({

                "path": path,

                "code": code

            })


            file_count += 1


        except Exception as e:

            logger.warning(

                f"skip file {path}: {str(e)}"

            )


    logger.info(

        f"files collected: {len(files)}"

    )


    return files