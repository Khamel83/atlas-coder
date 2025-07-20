# Getting Started

## Installation

```bash
# Clone the repository
git clone https://github.com/your-repo/atlas-coder.git
cd atlas-coder

# Set up Python environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Setup Options

**Option 1: Free Local Models (Recommended)**
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull a free model
ollama pull llama3.2
```

**Option 2: Free API Tiers**
```bash
# Set API key for OpenRouter free tier
echo "OPENAI_API_KEY=your-openrouter-key" > .env
```
