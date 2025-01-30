#!/usr/bin/env python3
import os
import argparse
import warnings
from pathlib import Path
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, WebsiteSearchTool
from langchain.tools import tool

# Warning control
warnings.filterwarnings('ignore')

# Load environment variables
env_path = Path('.env')
load_dotenv(dotenv_path=env_path)

def create_tools():
    """Create and return the tools for the agents."""
    # Tool for scraping CrewAI documentation
    docs_scrape_tool = ScrapeWebsiteTool(
        website_url="https://docs.crewai.com/how-to/Creating-a-Crew-and-kick-it-off/"
    )
    
    # Tool for general web search
    search_tool = SerperDevTool()
    
    # Tool for searching specific websites
    website_search_tool = WebsiteSearchTool()
    
    # Custom tool for checking customer history (example)
    @tool
    def check_customer_history(customer_name: str) -> str:
        """Check the customer's history of interactions and support tickets."""
        # This is a placeholder. In production, you would integrate with your CRM
        return f"Checking history for {customer_name}... This is a new customer."
    
    return [docs_scrape_tool, search_tool, website_search_tool, check_customer_history]

def create_agents(customer_name, tools):
    """Create and return the support and QA agents with tools and guardrails."""
    support_agent = Agent(
        role="Senior Support Representative",
        goal="Be the most friendly and helpful support representative in your team",
        backstory=(
            f"You work at crewAI (https://crewai.com) and are now working on providing "
            f"support to {customer_name}, a super important customer for your company. "
            "You need to make sure that you provide the best support! "
            "Make sure to provide full complete answers, and make no assumptions."
        ),
        allow_delegation=False,
        verbose=True,
        tools=tools,
        # Adding guardrails
        max_iter=3,  # Limit the number of iterations
        max_rpm=10,  # Rate limit for API calls
        temperature=0.7,  # Control randomness in responses
    )

    support_quality_assurance_agent = Agent(
        role="Support Quality Assurance Specialist",
        goal="Get recognition for providing the best support quality assurance in your team",
        backstory=(
            f"You work at crewAI (https://crewai.com) and are now working with your team "
            f"on a request from {customer_name} ensuring that the support representative is "
            "providing the best support possible.\n"
            "You need to make sure that the support representative is providing full "
            "complete answers, and make no assumptions."
        ),
        verbose=True,
        tools=tools,
        # Adding guardrails
        max_iter=2,  # Limit the number of iterations
        max_rpm=10,  # Rate limit for API calls
        temperature=0.5,  # More conservative for QA
    )

    return support_agent, support_quality_assurance_agent

def create_tasks(support_agent, qa_agent, customer_query):
    """Create and return the tasks for the agents."""
    handle_request = Task(
        description=(
            f"Handle the following customer request: {customer_query}\n"
            "1. First, use the docs_scrape_tool to check relevant documentation\n"
            "2. If needed, use search_tool for additional context\n"
            "3. Provide a clear, accurate, and helpful response\n"
            "4. Always verify information before sharing"
        ),
        expected_output="A clear, accurate, and helpful response to the customer's query",
        agent=support_agent
    )

    review_response = Task(
        description=(
            "Review the support agent's response and ensure it is complete, "
            "accurate, and helpful. Provide feedback if improvements are needed.\n"
            "1. Verify technical accuracy using documentation\n"
            "2. Check for completeness and clarity\n"
            "3. Ensure the tone is appropriate\n"
            "4. Suggest improvements if needed"
        ),
        expected_output="A quality assessment of the support response with any necessary improvement suggestions",
        agent=qa_agent
    )

    return [handle_request, review_response]

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Run customer support agent with CrewAI')
    parser.add_argument('customer_name', type=str, help='Name of the customer')
    parser.add_argument('query', type=str, help='Customer query or request')
    parser.add_argument('--openai-api-key', type=str, help='OpenAI API key', 
                      default=os.getenv('OPENAI_API_KEY'))
    parser.add_argument('--model', type=str, 
                      default=os.getenv('OPENAI_MODEL_NAME', 'gpt-3.5-turbo'),
                      help='OpenAI model to use (default: from .env or gpt-3.5-turbo)')
    parser.add_argument('--memory-file', type=str,
                      default='support_memory.json',
                      help='File to store conversation memory')
    
    args = parser.parse_args()

    # Validate OpenAI API key
    if not args.openai_api_key:
        raise ValueError("OpenAI API key is required. Set it in .env file or pass via --openai-api-key")

    # Set OpenAI configuration
    os.environ["OPENAI_API_KEY"] = args.openai_api_key
    os.environ["OPENAI_MODEL_NAME"] = args.model

    # Create tools
    tools = create_tools()

    # Create agents
    support_agent, qa_agent = create_agents(args.customer_name, tools)

    # Create tasks
    tasks = create_tasks(support_agent, qa_agent, args.query)

    # Create and run the crew with memory
    crew = Crew(
        agents=[support_agent, qa_agent],
        tasks=tasks,
        verbose=True,
        memory=True
    )

    # Run the crew and get results
    result = crew.kickoff()
    print("\nFinal Response:")
    print(result)

if __name__ == "__main__":
    main()
