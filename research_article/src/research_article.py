#!/usr/bin/env python3
import os
import argparse
import warnings
from pathlib import Path
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from rich.markdown import Markdown
from rich.console import Console

# Warning control
warnings.filterwarnings('ignore')

# Load environment variables
env_path = Path('.env')
load_dotenv(dotenv_path=env_path)

def create_agents():
    """Create and return the three agents: planner, writer, and editor."""
    planner = Agent(
        role="Content Planner",
        goal="Plan engaging and factually accurate content on {topic}",
        backstory="You're working on planning a blog article "
                 "about the topic: {topic}."
                 "You collect information that helps the "
                 "audience learn something "
                 "and make informed decisions. "
                 "Your work is the basis for "
                 "the Content Writer to write an article on this topic.",
        allow_delegation=False,
        verbose=True
    )

    writer = Agent(
        role="Content Writer",
        goal="Write insightful and factually accurate "
             "opinion piece about the topic: {topic}",
        backstory="You're working on a writing "
                 "a new opinion piece about the topic: {topic}. "
                 "You base your writing on the work of "
                 "the Content Planner, who provides an outline "
                 "and relevant context about the topic. "
                 "You follow the main objectives and "
                 "direction of the outline, "
                 "as provide by the Content Planner. "
                 "You also provide objective and impartial insights "
                 "and back them up with information "
                 "provide by the Content Planner. "
                 "You acknowledge in your opinion piece "
                 "when your statements are opinions "
                 "as opposed to objective statements.",
        allow_delegation=False,
        verbose=True
    )

    editor = Agent(
        role="Editor",
        goal="Edit a given blog post to align with "
             "the writing style of the organization. ",
        backstory="You are an editor who receives a blog post "
                 "from the Content Writer. "
                 "Your goal is to review the blog post "
                 "to ensure that it follows journalistic best practices,"
                 "provides balanced viewpoints "
                 "when providing opinions or assertions, "
                 "and also avoids major controversial topics "
                 "or opinions when possible.",
        allow_delegation=False,
        verbose=True
    )

    return planner, writer, editor

def create_tasks(planner, writer, editor):
    """Create and return the three tasks: plan, write, and edit."""
    plan = Task(
        description=(
            "1. Prioritize the latest trends, key players, "
                "and noteworthy news on {topic}.\n"
            "2. Identify the target audience, considering "
                "their interests and pain points.\n"
            "3. Develop a detailed content outline including "
                "an introduction, key points, and a call to action.\n"
            "4. Include SEO keywords and relevant data or sources."
        ),
        expected_output="A comprehensive content plan document "
            "with an outline, audience analysis, "
            "SEO keywords, and resources.",
        agent=planner,
    )

    write = Task(
        description=(
            "1. Use the content plan to craft a compelling "
                "blog post on {topic}.\n"
            "2. Incorporate SEO keywords naturally.\n"
            "3. Sections/Subtitles are properly named "
                "in an engaging manner.\n"
            "4. Ensure the post is structured with an "
                "engaging introduction, insightful body, "
                "and a summarizing conclusion.\n"
            "5. Proofread for grammatical errors and "
                "alignment with the brand's voice.\n"
        ),
        expected_output="A well-written blog post "
            "in markdown format, ready for publication, "
            "each section should have 2 or 3 paragraphs.",
        agent=writer,
    )

    edit = Task(
        description=("Proofread the given blog post for "
                     "grammatical errors and "
                     "alignment with the brand's voice."),
        expected_output="A well-written blog post in markdown format, "
                        "ready for publication, "
                        "each section should have 2 or 3 paragraphs.",
        agent=editor
    )

    return plan, write, edit

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Generate a research article using CrewAI')
    parser.add_argument('topic', type=str, help='The topic to research and write about')
    parser.add_argument('--openai-api-key', type=str, help='OpenAI API key', 
                      default=os.getenv('OPENAI_API_KEY'))
    parser.add_argument('--model', type=str, 
                      default=os.getenv('OPENAI_MODEL_NAME', 'gpt-3.5-turbo'),
                      help='OpenAI model to use (default: from .env or gpt-3.5-turbo)')
    
    args = parser.parse_args()

    # Validate OpenAI API key
    if not args.openai_api_key:
        raise ValueError("OpenAI API key is required. Set it in .env file or pass via --openai-api-key")

    # Set OpenAI configuration
    os.environ["OPENAI_API_KEY"] = args.openai_api_key
    os.environ["OPENAI_MODEL_NAME"] = args.model

    # Create agents and tasks
    planner, writer, editor = create_agents()
    plan, write, edit = create_tasks(planner, writer, editor)

    # Create and run the crew
    crew = Crew(
        agents=[planner, writer, editor],
        tasks=[plan, write, edit],
        verbose=True
    )

    # Run the crew and get results
    result = crew.kickoff(inputs={"topic": args.topic})

    # Display results using rich for beautiful markdown formatting
    console = Console()
    console.print(Markdown(str(result)))

if __name__ == "__main__":
    main() 