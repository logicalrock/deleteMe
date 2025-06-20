#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status

echo "🧹 Cleaning up nested project structure..."

# Move everything from the inner deleteMeWeb up to the current directory
mv deleteMeWeb/app ./app
mv deleteMeWeb/README.md ./README_web.md
mv deleteMeWeb/requirements.txt ./requirements_web.txt

# Remove the nested folder
rm -rf deleteMeWeb

# Optional cleanup for old or orphaned main.py
if grep -q "FastAPI" main.py; then
    echo "⚠️ Keeping main.py in root (seems valid FastAPI app)"
else
    echo "🗑 Removing old main.py (not used)"
    rm -f main.py
fi

# Git staging if inside a git repo
if [ -d ".git" ]; then
    git add -A
    echo "✅ Files staged. Run 'git commit -m \"Flatten project structure\"' when ready."
fi

echo "✅ Cleanup complete. Your project structure is now flat and clean."

