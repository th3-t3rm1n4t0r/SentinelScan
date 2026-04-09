import httpx
import asyncio
import logging
import base64
from typing import List, Dict, Optional

from app.config import settings


logger = logging.getLogger("sentinel_scan.github")


# =========================
# SETTINGS
# =========================

SUPPORTED_EXTENSIONS = (
    ".py",
    ".js",
    ".ts",
    ".java",
    ".go",
    ".rs",
    ".php",
    ".cs",
    ".cpp",
    ".c",
    ".jsx",
    ".tsx",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".env"
)

MAX_FILES = getattr(settings, "MAX_FILES", 120)
MAX_FILE_SIZE_KB = getattr(settings, "MAX_FILE_SIZE_KB", 200)


# =========================
# MAIN ENTRY
# =========================

def get_repo_tree(
    repo_url: str,
    branch: Optional[str] = None
) -> List[Dict]:

    owner, repo = extract_owner_repo(repo_url)

    branch = branch or getattr(settings, "GITHUB_DEFAULT_BRANCH", "main")

    logger.info(f"Fetching repo tree {owner}/{repo}@{branch}")

    tree_url = (
        f"{settings.GITHUB_API_BASE}/repos/"
        f"{owner}/{repo}/git/trees/{branch}?recursive=1"
    )

    headers = build_headers()

    try:

        response = httpx.get(
            tree_url,
            headers=headers,
            timeout=40
        )

        if response.status_code == 404:
            raise Exception(
                f"Repository or branch not found: {repo}@{branch}"
            )

        response.raise_for_status()

    except Exception as e:

        logger.error(
            f"GitHub tree fetch failed: {str(e)}"
        )

        raise


    tree = response.json().get("tree", [])

    file_urls = []


    for item in tree:

        if item.get("type") != "blob":
            continue


        file_path = item.get("path", "")


        if not file_path.endswith(SUPPORTED_EXTENSIONS):
            continue


        if item.get("size", 0) > MAX_FILE_SIZE_KB * 1024:
            continue


        file_urls.append(
            item.get("url")
        )


        if len(file_urls) >= MAX_FILES:
            break


    logger.info(
        f"Files selected for scan: {len(file_urls)}"
    )


    return run_async_download(
        file_urls,
        headers
    )


# =========================
# ASYNC DOWNLOAD
# =========================

def run_async_download(
    urls: List[str],
    headers: Dict
):

    return asyncio.run(
        fetch_all_files(
            urls,
            headers
        )
    )


async def fetch_all_files(
    urls: List[str],
    headers: Dict
):

    async with httpx.AsyncClient(timeout=40) as client:

        tasks = [

            fetch_file(
                client,
                url,
                headers
            )

            for url in urls

        ]


        results = await asyncio.gather(
            *tasks,
            return_exceptions=True
        )


        return [

            r for r in results

            if isinstance(r, dict)

        ]


async def fetch_file(
    client: httpx.AsyncClient,
    url: str,
    headers: Dict
):

    try:

        response = await client.get(
            url,
            headers=headers
        )

        response.raise_for_status()

        data = response.json()


        return {

            "path":

            data.get("path"),


            "content":

            decode_base64(

                data.get("content", "")

            )

        }


    except Exception as e:

        logger.warning(

            f"File fetch failed {url} | {str(e)}"

        )

        return None


# =========================
# HELPERS
# =========================

def extract_owner_repo(
    repo_url: str
):

    parts = repo_url.rstrip("/").split("/")

    return parts[-2], parts[-1]


def decode_base64(
    content: str
):

    try:

        return base64.b64decode(
            content
        ).decode(
            "utf-8",
            errors="ignore"
        )

    except Exception:

        return ""


def build_headers():

    token = getattr(settings, "GITHUB_TOKEN", None)

    if token:

        return {

            "Authorization":
            f"Bearer {token}"

        }


    return {} 
