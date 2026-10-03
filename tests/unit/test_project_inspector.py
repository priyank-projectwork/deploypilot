from app.tools.project_inspector import inspect_project


def test_inspector_returns_project_root():
    result = inspect_project(".")

    assert "Project root:" in result


def test_inspector_lists_agent_file():
    result = inspect_project(".")

    assert "app/agent.py" in result


def test_inspector_lists_reader_file():
    result = inspect_project(".")

    assert "app/tools/project_reader.py" in result


def test_inspector_excludes_sensitive_files():
    result = inspect_project(".")

    assert ".env" not in result
    assert "session.db" not in result
