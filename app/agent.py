from google.adk.agents import Agent
from google.adk.apps import App

MODEL = "gemini-3.8-flash"

root_agent = Agent(
    name="deploypilot_agent",
    model=MODEL,
    instruction=(
        "You are DeployPilot, an AI assistant for investigating "
        "software deployment problems. "
        "For this initial prototype, answer clearly and concisely. "
        "Do not claim to have inspected external systems or deployment "
        "data unless a tool actually provides that information."
    ),
)

app = App(
    root_agent=root_agent,
    name="app",
)
