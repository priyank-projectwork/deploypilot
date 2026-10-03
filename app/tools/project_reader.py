from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

IGNORED_DIRS = {
    ".git",
    ".venv",
    ".adk",
    "__pycache__",
    "node_modules",
    ".idea",
    ".vscode",
}

IGNORED_FILES = {
    ".env",
    ".env.local",
    ".env.development",
    ".env.production",
}


def _resolve_project_path(path: str) -> Path | None:
    """Resolve a path and ensure it remains inside the project root."""
    candidate = Path(path)

    if not candidate.is_absolute():
        candidate = PROJECT_ROOT / candidate

    resolved = candidate.expanduser().resolve()

    try:
        resolved.relative_to(PROJECT_ROOT)
    except ValueError:
        return None

    return resolved


def read_project_file(path: str, max_chars: int = 12000) -> str:
    """Read a project text file for deployment investigation.

    Use this tool when you need the contents of a specific project file
    after identifying it as relevant. The tool is read-only, blocks
    sensitive files and ignored directories, and limits the amount of
    content returned to the model.
    """
    file_path = _resolve_project_path(path)

    if file_path is None:
        return "Access denied: path is outside the DeployPilot project."

    if not file_path.exists():
        return f"File does not exist: {file_path.relative_to(PROJECT_ROOT)}"

    if not file_path.is_file():
        return f"Path is not a file: {file_path.relative_to(PROJECT_ROOT)}"

    relative = file_path.relative_to(PROJECT_ROOT)

    if file_path.name in IGNORED_FILES:
        return "Access denied: sensitive environment file."

    if any(part in IGNORED_DIRS for part in relative.parts):
        return "Access denied: protected project path."

    try:
        content = file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return f"File is not a UTF-8 text file: {relative}"
    except OSError as exc:
        return f"Unable to read file: {exc}"

    if len(content) > max_chars:
        return (
            f"File: {relative}\n"
            f"Content truncated to {max_chars} characters.\n\n"
            f"{content[:max_chars]}"
        )

    return f"File: {relative}\n\n{content}"
