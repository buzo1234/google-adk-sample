from google.adk.agents import Agent, LoopAgent
from google.adk.tools import google_search

from ..config import config
from ..agent_utils import suppress_output_callback
from ..validation_checkers import OutlineValidationChecker

blog_planner = Agent(
    model=config.worker_model,
    name="blog_planner",
    description="Generates a blog post outline.",
    instruction="""
    You are a technical content strategist. Your job is to create a blog post outline.
    The outline should be well-structured and easy to follow.
    It should include a title, an introduction, a main body with several sections, and a conclusion.
    If a codebase is provided, the outline should include sections for code snippets and technical deep dives.
    The codebase context will be available in the `codebase_context` state key.
    Use the information in the `codebase_context` to generate a specific and accurate outline.
    Use Google Search to find relevant information and examples to support your writing.
    Your final output should be a blog post outline in Markdown format.
    """,
    tools=[google_search],
    output_key="blog_outline",
    after_agent_callback=suppress_output_callback,
)

robust_blog_planner = LoopAgent(
    name="robust_blog_planner",
    description="A robust blog planner that retries if it fails.",
    sub_agents=[
        blog_planner,
        OutlineValidationChecker(name="outline_validation_checker"),
    ],
    max_iterations=3,
    after_agent_callback=suppress_output_callback,
)
