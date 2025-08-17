# Movie Reviews Analysis Tool

This tool fetches and analyzes movie reviews using IMDB's public dataset in BigQuery and OpenAI's API for sentiment analysis.

## Setup Instructions

### 1. Python Environment Setup

First, create and activate a new Python virtual environment:

```bash
# Using venv (Python 3.8+ recommended)
python -m venv .venv

# Activate the virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate
```

### 2. Install Package

Install the package in editable mode:

```bash
pip install -e .
```

### 3. Credentials Setup

The application requires two API credentials:
1. Google Cloud credentials (for BigQuery access)
2. OpenAI API key (for sentiment analysis)

Create a `vars.env` file in the root directory of the project:

```bash
# Create vars.env file
touch vars.env
```

Add the following environment variables to `vars.env`:

```env
# Google Cloud credentials
GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/google-credentials.json"

# OpenAI API key
OPENAI_API_KEY="your-openai-api-key"

```


## Usage

Run the application locally:
```bash
python main.py
```

### Run the Streamlit Application

To run the interactive Streamlit application, execute the following command:

```bash
streamlit run streamlit_app.py
```

## Testing

Run all tests:
```bash
python -m pytest tests/
```

Or test specific components:
```bash
python -m pytest -v -s tests/test_agents.py  # Test all agents
python -m pytest -v -s tests/test_summary_agent.py  # Test just the summary agent
python -m pytest -v -s tests/test_tag_agent.py  # Test just the tag agent
```




