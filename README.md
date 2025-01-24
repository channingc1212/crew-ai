# CrewAI Research Article Generator

This tool uses CrewAI to generate research articles on any topic using a team of AI agents (planner, writer, and editor).

## Installation

1. Clone this repository
2. Install the required packages:
```bash
pip install -r requirement.txt
```

3. Set up your environment:
```bash
cp .env.example .env
```
Then edit `.env` and add your OpenAI API key.

## Configuration

The tool uses environment variables for configuration. You can set these in your `.env` file:

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `OPENAI_MODEL_NAME`: The OpenAI model to use (default: gpt-3.5-turbo)

## Usage

### Basic Usage
```bash
python research_article.py "Your Topic Here"
```

### Advanced Usage
You can override the environment variables using command line arguments:
```bash
python research_article.py "Your Topic Here" --openai-api-key "your-key-here" --model "gpt-4"
```

### Arguments
- `topic` (required): The topic to research and write about
- `--openai-api-key`: Your OpenAI API key (optional if set in .env)
- `--model`: OpenAI model to use (optional if set in .env)

## Output
The script will output a beautifully formatted markdown article in your terminal, with proper formatting and structure.

## Security Note
The `.env` file contains sensitive information and is excluded from git tracking. Never commit your actual API keys to version control. 