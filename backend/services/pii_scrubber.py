import httpx
import asyncio
import logging
import base64

from typing import List, Dict

from app.config import settings


logger = logging.getLogger(
    "sentinel_scan.github"
)


# =========================
# SETTINGS
# =========================

MAX_FILES = settings.MAX_FILES

MAX_FILE_SIZE_KB = settings.MAX_FILE_SIZE_KB

MAX_CONCURRENT_REQUESTS = 10


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
    ".rb",
    ".swift",
    ".kt",
    ".sql",
    ".json",
    ".yaml",
    ".yml",
    ".xml",
    ".env",
    ".ini",
    ".cfg",
    ".toml"

)


# =========================
# PUBLIC ENTRY
# =========================

def get_repo_tree(repo_url: str) -> List[Dict]:

    owner, repo = extract_owner_repo(
        repo_url
    )

    headers = build_headers()

    default_branch = get_default_branch(
        owner,
        repo,
        headers
    )

    tree_url = f"{settings.GITHUB_API_BASE}/repos/{owner}/{repo}/git/trees/{default_branch}?recursive=1"


    tree_data = safe_request(
        tree_url,
        headers
    ).get("tree", [])


    file_urls = []

    for item in tree_data:

        if item.get("type") != "blob":
            continue

        path = item.get("path", "")

        size = item.get("size", 0)

        if not is_supported_file(path):
            continue

        if size > MAX_FILE_SIZE_KB * 1024:
            continue

        file_urls.append(
            item["url"]
        )

        if len(file_urls) >= MAX_FILES:
            break


    logger.info(
        f"{repo}@{default_branch} → {len(file_urls)} files"
    )


    files = run_async_fetch(
        file_urls,
        headers
    )


    return [
        f for f in files
        if f is not None
    ]


# =========================
# SAFE REQUEST
# =========================

def safe_request(
    url,
    headers,
    retries=2
):

    for attempt in range(
        retries + 1
    ):

        try:

            r = httpx.get(
                url,
                headers=headers,
                timeout=30
            )

            r.raise_for_status()

            return r.json()

        except Exception as e:

            logger.warning(
                f"GitHub retry {attempt+1} failed: {str(e)}"
            )

    raise Exception(
        "GitHub API request failed"
    )


# =========================
# ASYNC EXECUTION
# =========================

def run_async_fetch(
    urls: List[str],
    headers: Dict
):

    try:

        loop = asyncio.get_event_loop()

        if loop.is_running():

            return asyncio.run(
                fetch_all_files(
                    urls,
                    headers
                )
            )

        else:

            return loop.run_until_complete(
                fetch_all_files(
                    urls,
                    headers
                )
            )

    except RuntimeError:

        return asyncio.run(
            fetch_all_files(
                urls,
                headers
            )
        )


# =========================
# CONCURRENT FETCH
# =========================

async def fetch_all_files(
    urls,
    headers
):

    semaphore = asyncio.Semaphore(
        MAX_CONCURRENT_REQUESTS
    )

    async with httpx.AsyncClient(
        timeout=30
    ) as client:

        tasks = [

            fetch_file(
                client,
                url,
                headers,
                semaphore
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
    client,
    url,
    headers,
    semaphore
):

    async with semaphore:

        try:

            r = await client.get(
                url,
                headers=headers
            )

            r.raise_for_status()

            data = r.json()

            return {

                "path": data.get("path"),

                "content": decode_base64(
                    data.get("content")
                )

            }

        except Exception as e:

            logger.warning(
                f"fetch failed {url} | {str(e)}"
            )

            return None


# =========================
# HELPERS
# =========================

def extract_owner_repo(
    repo_url
):

    parts = repo_url.rstrip(
        "/"
    ).split("/")

    if len(parts) < 2:

        raise Exception(
            "Invalid GitHub URL"
        )

    return parts[-2], parts[-1]


def build_headers():

    headers = {

        "Accept": "application/vnd.github+json"

    }

    if settings.GITHUB_TOKEN:

        headers["Authorization"] = (

            f"Bearer {settings.GITHUB_TOKEN}"

        )

    return headers


def get_default_branch(
    owner,
    repo,
    headers
):

    url = f"{settings.GITHUB_API_BASE}/repos/{owner}/{repo}"

    return safe_request(
        url,
        headers
    ).get(
        "default_branch",
        "main"
    )


def is_supported_file(
    path
):

    return path.endswith(
        SUPPORTED_EXTENSIONS
    )


def decode_base64(
    content
):

    if not content:
        return ""

    try:

        return base64.b64decode(
            content
        ).decode(
            "utf-8",
            errors="ignore"
        )

    except Exception:

        return ""  