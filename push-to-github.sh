#!/bin/bash

# PrimeAI Push to GitHub Script

set -e

USERNAME="BILLY-KIMONO"
REPO_NAME="primeai"

echo "🚀 PrimeAI GitHub Push Setup"
echo "============================"
echo ""
echo "Username: $USERNAME"
echo "Repository: $REPO_NAME"
echo ""

# Step 1: Rename branch to main
echo "📝 Renaming master branch to main..."
git branch -M main

# Step 2: Check if repo exists
echo ""
echo "⏳ Checking GitHub repository..."
echo ""
echo "📌 IMPORTANT: Create the repository on GitHub first!"
echo ""
echo "Steps:"
echo "1. Go to: https://github.com/new"
echo "2. Repository name: primeai"
echo "3. Description: Anti-detect browser extension for interviews"
echo "4. Set to Public (recommended for launch)"
echo "5. Click 'Create repository'"
echo ""
echo "6. Come back here and press ENTER"
echo ""
read -p "Press ENTER once you've created the repository on GitHub..."

# Step 3: Add remote and push
REPO_URL="https://github.com/$USERNAME/$REPO_NAME.git"

echo ""
echo "🔗 Adding GitHub remote: $REPO_URL"
git remote add origin "$REPO_URL"

echo ""
echo "🔑 Authenticate with GitHub (one-time setup)..."
echo ""
echo "You have two options:"
echo "1. Use GitHub CLI (recommended): just type 'gh' when prompted"
echo "2. Use Personal Access Token (PAT): create one at settings/developer-settings/personal-access-tokens"
echo ""
echo "📤 Pushing code to GitHub..."
git push -u origin main

echo ""
echo "✅ SUCCESS! Your code is now on GitHub!"
echo ""
echo "🔗 Your repository: https://github.com/$USERNAME/$REPO_NAME"
echo ""
echo "Next steps:"
echo "1. Choose deployment method (see README.md)"
echo "2. Setup GitHub Actions CI/CD (optional)"
echo "3. Publish to Chrome & Firefox stores"
echo ""
