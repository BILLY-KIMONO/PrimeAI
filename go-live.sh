#!/bin/bash

# 🚀 PrimeAI Live Deployment - Interactive Setup

set -e

echo ""
echo "🛡️  PrimeAI - Make It Live Setup"
echo "=================================="
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
  echo "❌ Git is not installed. Install it first:"
  echo "   macOS: brew install git"
  echo "   Ubuntu: sudo apt-get install git"
  exit 1
fi

echo "📋 Choose your deployment method:"
echo ""
echo "1) GitHub + Auto-Deploy (CI/CD) - RECOMMENDED"
echo "2) Heroku (Fastest, ready in 30min)"
echo "3) AWS EC2 (Manual setup)"
echo "4) DigitalOcean (Good balance)"
echo "5) Local Testing Only"
echo ""
read -p "Enter choice (1-5): " choice

case $choice in
  1)
    echo ""
    echo "🔧 Setting up GitHub + CI/CD"
    echo "============================"
    echo ""
    
    # Initialize git
    echo "📝 Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial commit: PrimeAI Interview Shield v1.0"
    
    echo ""
    echo "🔗 GitHub Repository Setup:"
    echo "1. Go to https://github.com/new"
    echo "2. Create repo: 'primeai'"
    echo "3. Copy the HTTPS URL"
    echo ""
    read -p "Paste your GitHub HTTPS URL: " github_url
    
    git remote add origin "$github_url"
    git branch -M main
    git push -u origin main
    
    echo ""
    echo "✅ Code pushed to GitHub!"
    echo ""
    echo "🔐 Setup GitHub Secrets:"
    echo "1. Go to: Settings → Secrets and variables → Actions"
    echo "2. Click 'New repository secret' and add:"
    echo ""
    echo "   DOCKER_USERNAME: docker-hub-username"
    echo "   DOCKER_PASSWORD: docker-hub-token"
    echo "   STRIPE_SECRET_KEY: sk_live_..."
    echo "   DATABASE_PASSWORD: your-secure-password"
    echo "   SECRET_KEY: $(openssl rand -hex 16)"
    echo ""
    echo "   For deployment:"
    echo "   PROD_HOST: your-server-ip"
    echo "   PROD_USER: ubuntu"
    echo "   PROD_SSH_KEY: (your SSH private key)"
    echo ""
    echo "3. Copy .github/workflows/deploy.yml from project"
    echo ""
    echo "✨ GitHub Actions CI/CD is ready!"
    echo "Every git push to main will auto-deploy"
    ;;
    
  2)
    echo ""
    echo "⚡ Setting up Heroku"
    echo "==================="
    echo ""
    
    if ! command -v heroku &> /dev/null; then
      echo "📥 Installing Heroku CLI..."
      curl https://cli.heroku.com/install.sh | sh
    fi
    
    echo "Login to Heroku..."
    heroku login
    
    echo ""
    read -p "Enter app name (e.g., primeai-app): " app_name
    
    echo "📱 Creating Heroku app..."
    heroku create "$app_name"
    
    echo "🗄️  Adding database addons..."
    heroku addons:create heroku-postgresql:standard-0 -a "$app_name"
    heroku addons:create heroku-redis:premium-0 -a "$app_name"
    
    echo ""
    echo "🔐 Setting environment variables..."
    read -p "Enter SECRET_KEY: " secret_key
    read -p "Enter STRIPE_SECRET_KEY: " stripe_key
    
    heroku config:set SECRET_KEY="$secret_key" -a "$app_name"
    heroku config:set STRIPE_SECRET_KEY="$stripe_key" -a "$app_name"
    
    echo "📦 Creating Procfile..."
    cat > Procfile << 'EOF'
web: cd backend && gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
EOF
    
    echo ""
    echo "📤 Deploying to Heroku..."
    git push heroku main
    
    echo ""
    echo "✅ Heroku deployment complete!"
    echo "   Your app is live at: https://$app_name.herokuapp.com"
    echo ""
    echo "📊 View logs:"
    echo "   heroku logs -f -a $app_name"
    ;;
    
  3)
    echo ""
    echo "🔧 AWS EC2 Setup"
    echo "================"
    echo ""
    echo "Manual steps:"
    echo "1. Go to AWS Console → EC2"
    echo "2. Launch instance: Ubuntu 22.04 LTS"
    echo "3. Instance type: t3.medium (minimum)"
    echo "4. Security group: Allow 80, 443, 22"
    echo ""
    read -p "Enter your EC2 instance IP: " ec2_ip
    
    echo ""
    echo "📝 Creating deployment script..."
    cat > /tmp/setup-aws.sh << 'EOFSCRIPT'
#!/bin/bash
set -e

echo "🚀 Setting up AWS EC2..."

sudo apt-get update
sudo apt-get upgrade -y

echo "📦 Installing dependencies..."
sudo apt-get install -y \
  curl git python3-pip postgresql postgresql-contrib redis-server nginx certbot python3-certbot-nginx

echo "🐳 Installing Docker..."
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

echo "📂 Cloning PrimeAI..."
git clone <your-github-url> /app/primeai
cd /app/primeai

echo "⚙️  Configuring environment..."
cp backend/.env.example backend/.env
echo "📝 Edit backend/.env with your credentials, then run: ./deploy.sh"

echo "✅ AWS EC2 ready for deployment!"
EOFSCRIPT
    
    echo "🔐 Copying setup script to EC2..."
    scp /tmp/setup-aws.sh "ubuntu@$ec2_ip:/tmp/"
    
    echo "🚀 Running setup on EC2..."
    ssh "ubuntu@$ec2_ip" "bash /tmp/setup-aws.sh"
    
    echo ""
    echo "✅ AWS setup complete!"
    echo "   SSH into server: ssh ubuntu@$ec2_ip"
    echo "   Deploy with: ./deploy.sh"
    ;;
    
  4)
    echo ""
    echo "🌊 DigitalOcean App Platform"
    echo "============================"
    echo ""
    echo "Quick setup:"
    echo "1. Go to DigitalOcean → App Platform"
    echo "2. Connect GitHub repo"
    echo "3. Select 'primeai' repository"
    echo "4. Configure:"
    echo "   - Basic: Node.js 18 for frontend"
    echo "   - API: Python 3.11 for backend"
    echo "   - Database: PostgreSQL 15"
    echo "   - Cache: Redis"
    echo "5. Deploy!"
    echo ""
    echo "📖 Full guide: https://docs.digitalocean.com/products/app-platform/"
    ;;
    
  5)
    echo ""
    echo "🧪 Local Testing Setup"
    echo "====================="
    echo ""
    echo "Starting services locally..."
    
    docker-compose up -d
    
    sleep 5
    
    echo ""
    echo "✅ Services running:"
    echo "   Frontend:  http://localhost:3000"
    echo "   Backend:   http://localhost:8000"
    echo "   API Docs:  http://localhost:8000/docs"
    echo "   Database:  postgresql://localhost:5432"
    echo "   Redis:     redis://localhost:6379"
    echo ""
    echo "📝 Test the API:"
    echo "   curl http://localhost:8000/health"
    echo ""
    ;;
    
  *)
    echo "❌ Invalid choice"
    exit 1
    ;;
esac

echo ""
echo "📚 Next Steps:"
echo "1. Configure domain DNS"
echo "2. Setup SSL/HTTPS"
echo "3. Enable payment processing (Stripe)"
echo "4. Setup monitoring (UptimeRobot, Sentry)"
echo "5. Publish browser extensions to stores"
echo ""
echo "📖 Full guide: PRODUCTION_GUIDE.md"
echo ""
