# 🔗 How to Push PrimeAI to GitHub

## Starting Fresh: Setup GitHub & Push Code

### Step 1: Create GitHub Account
1. Go to https://github.com/join
2. Create account (or login if you have one)
3. Go to https://github.com/new

### Step 2: Create Repository
1. **Repository name**: `primeai`
2. **Description**: "Anti-detect browser extension for interviews"
3. **Visibility**: Public (better for launches) or Private
4. **Initialize with**: Leave blank (we'll push existing code)
5. Click **Create repository**

You'll see a page with commands. Copy the HTTPS URL.

---

## Step 3: Push Your Code

Open terminal and run:

```bash
# Navigate to project
cd /home/bill-fardan/PrimeAI

# Initialize git (if not already done)
git init

# Configure git with your GitHub credentials
git config --global user.name "Your Name"
git config --global user.email "your-email@github.com"

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: PrimeAI Interview Shield v1.0 🛡️

- Backend: FastAPI + PostgreSQL + Redis
- Frontend: HTML5/JS dashboard
- Extension: Chrome/Firefox browser extension
- Anti-detect: 5-layer stealth protection
- Pricing: $8/month + 1-day free trial
- Production-ready deployment included"

# Add GitHub remote (replace with your URL from Step 2)
git remote add origin https://github.com/YOUR-USERNAME/primeai.git

# Rename branch to main (GitHub standard)
git branch -M main

# Push to GitHub
git push -u origin main
```

---

## Step 4: Verify on GitHub

1. Go to your repository: https://github.com/YOUR-USERNAME/primeai
2. You should see all your files
3. Check that everything is there:
   ```
   ✅ backend/
   ✅ extension/
   ✅ frontend/
   ✅ docker-compose.yml
   ✅ README.md
   ✅ All guides (PRODUCTION_GUIDE.md, etc.)
   ```

---

## Now: Choose Deployment Method

### Option A: Heroku Auto-Deploy (Easiest)

```bash
# Make sure you're in the repo folder
cd /home/bill-fardan/PrimeAI

# Install Heroku CLI
curl https://cli.heroku.com/install.sh | sh

# Login to Heroku (you need to create account first at heroku.com)
heroku login

# Create app
heroku create primeai-app

# Add databases
heroku addons:create heroku-postgresql:standard-0
heroku addons:create heroku-redis:premium-0

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key-here
heroku config:set STRIPE_SECRET_KEY=sk_live_or_test_key

# Deploy from GitHub
git push heroku main

# Check deployment
heroku logs --tail

# Your app is live at: https://primeai-app.herokuapp.com
```

### Option B: AWS with GitHub Actions (Most Professional)

This auto-deploys every time you push to GitHub.

1. Create AWS EC2 instance (see PRODUCTION_GUIDE.md)
2. Add GitHub Secrets:
   - Go to repo → Settings → Secrets → Create these:
   ```
   PROD_HOST = your-ec2-ip
   PROD_USER = ubuntu
   PROD_SSH_KEY = (contents of your .pem file)
   DOCKER_USERNAME = your-dockerhub-username
   DOCKER_PASSWORD = your-dockerhub-password
   ```

3. Copy deployment workflow:
   ```bash
   # Create workflow directory
   mkdir -p .github/workflows
   
   # Copy the deploy.yaml file from PRODUCTION_GUIDE.md
   # Into: .github/workflows/deploy.yml
   ```

4. Push to GitHub:
   ```bash
   git add .github/
   git commit -m "Add GitHub Actions CI/CD pipeline"
   git push origin main
   ```

5. Now every push auto-deploys to AWS! 🚀

---

## Continue Development & Push Updates

After initial launch, to push code changes:

```bash
# Make your changes to files

# Check what changed
git status

# Stage changes
git add .

# Create commit
git commit -m "Feature: Add XYZ functionality"

# Push to GitHub
git push origin main

# If using GitHub Actions or Heroku, it auto-deploys!
```

---

## Common Git Commands

```bash
# Check current status
git status

# See commit history
git log

# See what's changed
git diff

# Commit specific file
git add path/to/file
git commit -m "message"

# Push to GitHub
git push origin main

# Pull latest from GitHub (if working with team)
git pull origin main

# Create a new branch for features
git checkout -b feature/new-feature
git add .
git commit -m "Feature: new feature"
git push origin feature/new-feature
# Then create Pull Request on GitHub

# Delete a branch
git branch -d feature/new-feature
```

---

## What Happens After You Push?

### With Heroku
```
You push to main
    ↓
GitHub received your code
    ↓
Heroku sees new push
    ↓
Heroku auto-builds Docker image
    ↓
Heroku runs deploy.sh
    ↓
Your app is updated ✅
    ↓
Users see new version
```

### With GitHub Actions + AWS
```
You push to main
    ↓
GitHub runs .github/workflows/deploy.yml
    ↓
Tests run
    ↓
Docker images built
    ↓
Images pushed to Docker Hub
    ↓
SSH into your AWS server
    ↓
Pull new Docker images
    ↓
Restart containers
    ↓
Your app is updated ✅
    ↓
Users see new version
```

---

## GitHub Tips

### Make README.md look better
GitHub renders markdown, so your README.md will be the homepage of your repo.

### Add badges
```markdown
[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue)](https://github.com/your-username/primeai)
[![Docker](https://img.shields.io/badge/Docker-Ready-brightgreen)](https://www.docker.com)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
```

### Create releases
```bash
# Tag a version
git tag v1.0.0
git push origin v1.0.0

# Then go to GitHub repo → Releases and publish it
```

### Publish to GitHub Pages (for docs)
```bash
# Create gh-pages branch
git checkout --orphan gh-pages

# Add your documentation files
git add .
git commit -m "Add documentation"
git push origin gh-pages

# Your docs are now at: https://your-username.github.io/primeai
```

---

## Next: Deploy

After pushing to GitHub, choose one option:

**Option 1: Heroku** (Fastest, 5 minutes)
```bash
heroku create primeai-app
git push heroku main
# → Live in 5 minutes
```

**Option 2: AWS + GitHub Actions** (Best, 2 hours setup then auto-deploy)
- See PRODUCTION_GUIDE.md

**Option 3: DigitalOcean App Platform** (Good balance, 1 hour)
- Connect GitHub repo directly
- Auto-deploys on pushes

---

## Show Off Your Repository

1. **Share the link**: "Check out my startup: https://github.com/you/primeai"
2. **Share your deployment**:
   - "My API is live: https://primeai-app.herokuapp.com"
   - "Try the dashboard: https://api.primeai-app.herokuapp.com"
3. **Put in your portfolio**: Link to your GitHub repo
4. **Share on Twitter**: "Just launched PrimeAI on GitHub: [link]"
5. **Post on Reddit**: r/webdev, r/python, r/FastAPI

---

## That's It! 🎉

You've now learned:
✅ How to create a GitHub repo
✅ How to push code to GitHub
✅ How to auto-deploy from GitHub
✅ How to make updates and push them

**Next**: Pick Heroku or AWS and deploy! See the deployment guides.
