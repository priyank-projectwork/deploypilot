from pathlib import Path

# Directories that should never be inspected or returned to the model.
IGNORED_DIRS = {
    ".git",
    ".venv",
    ".adk",
    "__pycache__",
    "node_modules",
    ".idea",
    ".vscode",
}

# Files that commonly contain secrets or sensitive local configuration.
IGNORED_FILES = {
    ".env",
    ".env.local",
    ".env.development",
    ".env.production",
}

# Files that are particularly useful when investigating deployments.
PRIORITY_FILES = {
    "Dockerfile",
    "docker-compose.yml",
    "docker-compose.yaml",
    "compose.yml",
    "compose.yaml",
    "package.json",
    "requirements.txt",
    "pyproject.toml",
    "render.yaml",
    "vercel.json",
    "railway.json",
    "Procfile",
}


def inspect_project(path: str = ".") -> str:
    """Inspect a project directory and return compact deployment-relevant file information.

    Use this tool when you need evidence from the user's project before diagnosing
    a deployment problem. The tool is read-only and never executes project code.
    Sensitive files, dependency caches, virtual environments, Git metadata, and
    other local runtime directories are excluded.
    """
    root = Path(path).expanduser().resolve()

    if not root.exists():
        return f"Project path does not exist: {root}"

    if not root.is_dir():
        return f"Project path is not a directory: {root}"

    files = []

    for candidate in root.rglob("*"):
        if not candidate.is_file():
            continue

        relative = candidate.relative_to(root)

        if any(part in IGNORED_DIRS for part in relative.parts):
            continue

        if candidate.name in IGNORED_FILES:
            continue

        files.append(relative)

    files.sort(
        key=lambda item: (
            0 if item.name in PRIORITY_FILES else 1,
            str(item).lower(),
        )
    )

    if not files:
        return "No inspectable project files were found."

    lines = [
        f"Project root: {root}",
        f"Inspectable files: {len(files)}",
        "",
        "Files:",
    ]

    for relative in files[:100]:
        marker = " [priority]" if relative.name in PRIORITY_FILES else ""
        lines.append(f"- {relative}{marker}")

    if len(files) > 100:
        lines.append(f"- ... {len(files) - 100} more files omitted")

    return "\n".join(lines)
