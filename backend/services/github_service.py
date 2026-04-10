
import os
import git

def clone_repo(url):
    folder = "repo"

    if os.path.exists(folder):
        return folder

    git.Repo.clone_from(url, folder)

    return folder
