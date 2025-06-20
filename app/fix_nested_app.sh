#!/bin/bash
echo "🚚 Moving core files up from app/app to app/..."

# Move everything from app/app/ up one level to app/
mv app/* .

# Remove the now-empty nested app/ directory
rmdir app

echo "✅ Done. Project structure is fixed. You can now run 'uvicorn app.main:app --reload' from project root."

