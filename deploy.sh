#!/bin/bash
# Deploy daniferr.com → Netlify via GitHub
# Uso: ./deploy.sh "descrizione delle modifiche"

set -e

cd "$(dirname "$0")"

MSG="${1:-update: aggiornamento sito}"

echo "📦 Staging modifiche..."
git add .

if git diff --cached --quiet; then
  echo "✅ Nessuna modifica da deployare."
  exit 0
fi

echo "💬 Commit: $MSG"
git commit -m "$MSG"

echo "🚀 Push su GitHub → Netlify..."
git push origin main

echo ""
echo "✅ Deploy avviato. Il sito sarà aggiornato in 1-2 minuti."
echo "👉 Verifica: https://daniferr.com"
