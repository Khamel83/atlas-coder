#!/bin/bash
# Initialize Atlas Coder with standard layout

echo "Initializing Atlas Coder..."
cp .env.template .env
mkdir -p logs scratch projects
touch logs/.gitkeep scratch/.gitkeep projects/.gitkeep
echo "Done. Now edit .env and you're ready."
