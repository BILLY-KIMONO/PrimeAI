#!/bin/bash
# Render.com Deployment Setup Script
# This script creates the configuration files needed for Render deployment

echo "🚀 Creating Render deployment configuration..."

# Create render.yaml
cat > render.yaml << 'EOF'
services:
  - type: web
    name: primeai-backend
    env: python
    plan: free
    buildCommand: "pip install -r requirements.txt"
    startCommand: "python -m uvicorn app.main:app --host 0.0.0.0 --port 8000"
    envVars:
      - key: PYTHONPATH
        value: "."
    rootDir: backend
    
databases:
  - name: primeai-postgres
    plan: free
    databaseName: primeai
    user: primeai
    region: oregon
EOF

echo "✅ Created render.yaml"

# Create Procfile for additional compatibility
cat > backend/Procfile << 'EOF'
web: python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
EOF

echo "✅ Created backend/Procfile"

# Git add and show status
git add render.yaml backend/Procfile
echo ""
echo "📝 Git status:"
git status

echo ""
echo "✅ Ready to deploy!"
echo ""
echo "Next steps:"
echo "1. Push to GitHub:"
echo "   git commit -m 'Add Render deployment configuration'"
echo "   git push"
echo ""
echo "2. Go to https://render.com"
echo "3. Click 'New +'"
echo "4. Select 'Web Service'"
echo "5. Connect your GitHub repo"
echo "6. Follow the steps on this document: RENDER_DEPLOY_STEPS.md"
