# Atlas Coder

A lightweight terminal-based assistant powered by OpenAI for fast local AI access on resource-constrained devices (e.g., Raspberry Pi).

## Features

- Simple CLI chat interface
- `.env` support for OpenAI API key
- Works on low-powered devices
- No telemetry or analytics

## Requirements

- Python 3.11+
- `openai==0.28.1`
- `python-dotenv`

## Setup

```bash
# Clone the repo
git clone git@github.com:Khamel83/bootstrap.git atlas-coder
cd atlas-coder

# Set up Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Add your OpenAI API key to a .env file
echo "OPENAI_API_KEY=your-key-here" > .env

# Run the assistant
python main.py

