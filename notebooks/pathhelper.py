import git
from pathlib import Path

def git_root(path: str | Path) -> Path:
    """Return the path to the root of the git repo contianing this directory."""    
    git_repo = git.Repo(path, search_parent_directories=True)
    git_root = Path(git_repo.git.rev_parse("--show-toplevel"))
    return git_root

def data_dir(path: str | Path) -> Path:
    """Return the path to the data directory under the git root containing this directory."""
    return git_root(path) / "data";