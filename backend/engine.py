import httpx
import base64
import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


# =========================
# ENV
# =========================

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

LLM_API_KEY = os.getenv("OPENAI_API_KEY")


# =========================
# GITHUB TREE
# =========================

async def get_repo_tree(

    owner: str,
    repo: str,
    sha: str

):

    url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{sha}?recursive=1"

    headers = {

        "Authorization": f"Bearer {GITHUB_TOKEN}"

    }

    async with httpx.AsyncClient() as client:

        r = await client.get(

            url,
            headers=headers

        )

    r.raise_for_status()

    return r.json()


# =========================
# FILTER FILES
# =========================

def filter_paths(tree):

    return [

        f["path"]

        for f in tree.get(

            "tree",
            []

        )

        if not any(

            x in f["path"]

            for x in [

                "docs/",
                "tests/",
                ".md",
                ".txt"

            ]

        )

    ]


# =========================
# GET FILE CONTENT
# =========================

async def get_file(

    owner: str,
    repo: str,
    path: str

):

    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"

    headers = {

        "Authorization": f"Bearer {GITHUB_TOKEN}"

    }

    async with httpx.AsyncClient() as client:

        r = await client.get(

            url,
            headers=headers

        )

    r.raise_for_status()

    data = r.json()

    content = data.get(

        "content",
        ""

    )

    if content:

        return base64.b64decode(

            content

        ).decode(

            "utf-8",
            errors="ignore"

        )

    return ""


# =========================
# SIMPLE AI MOCK
# =========================

def fake_llm_select(

    issue: str,
    paths: list[str]

):

    return paths[:3]


def fake_llm_fix(

    code: str

):

    return code.replace(

        "password=",

        "password=os.getenv('PASSWORD')"

    )


# =========================
# CREATE PR (MOCK)
# =========================

async def create_pr(

    owner: str,
    repo: str,
    sha: str

):

    return {

        "status": "created"

    }


# =========================
# PIPELINE
# =========================

async def run_pipeline(

    data: dict

):

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


        fixed_code = fake_llm_fix(

            code

        )


        fixes.append({

            "path": path,
            "code": fixed_code

        })


    await create_pr(

        data["repo_owner"],
        data["repo_name"],
        data["main_sha"]

    )


    return {

        "files_fixed": len(fixes),
        "status": "done"

    } 