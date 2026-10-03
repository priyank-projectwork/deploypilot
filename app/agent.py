from google.adk.agents import Agent
from google.adk.apps import App

from app.tools.project_inspector import inspect_project
from app.tools.project_reader import read_project_file

MODEL = "gemini-3.8-flash"

root_agent = Agent(
    name="deploypilot_agent",
    model=MODEL,
    instruction=(
        "You are DeployPilot, an AI assistant for investigating "
        "software deployment problems. "
        "Use project inspection tools when you need evidence from "
        "the user's project. "
        "First inspect the project to discover relevant files, then "
        "read only files that are relevant to the user's problem. "
        "Do not read sensitive environment files. "
        "Never claim to have inspected files unless you actually "
        "used an available tool. "
        "Never assume a deployment configuration exists without "
        "evidence. "
        "For this prototype, answer clearly and concisely."
    ),
    tools=[inspect_project, read_project_file],
)

app = App(
    root_agent=root_agent,
    name="app",
)
