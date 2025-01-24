# Research Article Generator

This project uses CrewAI to generate well-researched articles on any topic using a team of AI agents.

## Project Structure

```
research_article/
├── src/                    # Source code
│   └── research_article.py # Main script
├── docs/                   # Documentation
│   └── README.md          # Detailed documentation
├── .env.example           # Example environment variables
└── requirements.txt       # Project dependencies
```

## Quick Start

1. Clone the repository and navigate to the project directory:
   ```bash
   cd research_article
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your OpenAI API key
   ```

4. Run the script:
   ```bash
   python src/research_article.py "Your Topic"
   ```

## Features

- Multi-agent system using CrewAI
- Content planning, writing, and editing
- Beautiful markdown output
- SEO-optimized content
- Customizable OpenAI models

## Usage Examples

1. Generate an article:
   ```bash
   python src/research_article.py "The Impact of AI on Healthcare"
   ```

2. Use a specific OpenAI model:
   ```bash
   python src/research_article.py "Your Topic" --model "gpt-4"
   ```

3. Save output to a file:
   ```bash
   python src/research_article.py "Your Topic" > article.md
   ```

## Configuration

- `OPENAI_API_KEY`: Your OpenAI API key
- `OPENAI_MODEL_NAME`: The OpenAI model to use (default: gpt-3.5-turbo)

## Contributing

Feel free to submit issues and enhancement requests! 