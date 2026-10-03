from pathlib import Path

from app.tools.project_inspector import inspect_project
from app.tools.project_reader import read_project_file


FIXTURE_ROOT = (
    Path(__file__).parent
    / "fixtures"
    / "deployment_project"
)


def test_deployment_fixture_contains_dockerfile():
    result = inspect_project(str(FIXTURE_ROOT))

    assert "Dockerfile" in result
    assert "requirements.txt" in result
    assert "app.py" in result


def test_deployment_fixture_dockerfile_contains_runtime_configuration():
    result = read_project_file(
        str(FIXTURE_ROOT / "Dockerfile")
    )

    assert "FROM python:3.14-slim" in result
    assert 'CMD ["python", "app.py"]' in result
