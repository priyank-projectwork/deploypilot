from app.tools.project_reader import read_project_file


def test_reads_project_file():
    result = read_project_file("app/agent.py")

    assert "deploypilot_agent" in result
    assert "gemini-3.8-flash" in result


def test_blocks_environment_file():
    result = read_project_file(".env")

    assert result == "Access denied: sensitive environment file."


def test_blocks_adk_runtime_state():
    result = read_project_file("app/.adk/session.db")

    assert result == "Access denied: protected project path."


def test_blocks_path_outside_project():
    result = read_project_file("/tmp/test.txt")

    assert result == "Access denied: path is outside the DeployPilot project."


def test_handles_missing_file():
    result = read_project_file("does-not-exist.txt")

    assert result == "File does not exist: does-not-exist.txt"
