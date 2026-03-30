#!/bin/bash

echo "🚀 Switching to SSH and pushing to GitHub..."
echo ""

cd /home/bill-fardan/PrimeAI

# Switch from HTTPS to SSH remote
echo "1️⃣  Updating git remote to SSH..."
git remote set-url origin git@github.com:BILLY-KIMONO/primeai.git

# Test SSH connection
echo "2️⃣  Testing SSH connection to GitHub..."
if ssh -T git@github.com 2>&1 | grep -q "Hi BILLY-KIMONO"; then
    echo "✅ SSH connection successful!"
else
    echo "❌ SSH connection failed. Make sure you added the key to GitHub."
    exit 1
fi

# Push to GitHub
echo ""
echo "3️⃣  Pushing code to GitHub..."
git push -u origin main

echo ""
echo "✅ SUCCESS! Your code is now on GitHub!"
echo ""
echo "📍 Repository: https://github.com/BILLY-KIMONO/primeai"
