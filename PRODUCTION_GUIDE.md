# 🚀 PrimeAI - Make It Live

## Option 1: GitHub + CI/CD (Recommended)

### Step 1: Create GitHub Repository

```bash
cd /home/bill-fardan/PrimeAI

# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: PrimeAI Interview Shield v1.0"

# Add GitHub remote
git remote add origin https://github.com/YOUR-USERNAME/primeai.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 2: Setup GitHub Secrets (for CI/CD)

Go to GitHub repo → Settings → Secrets → New repository secret

Add these secrets:
```
DOCKER_USERNAME = your-dockerhub-username
DOCKER_PASSWORD = your-dockerhub-token
STRIPE_SECRET_KEY = sk_live_your_key
DATABASE_PASSWORD = secure_password_here
SECRET_KEY = your-jwt-secret-min-32-chars
```

### Step 3: Create GitHub Actions Workflow

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
      redis:
        image: redis:7
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s

    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      
      - name: Run tests
        run: |
          cd backend
          python -m pytest tests/

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Build Docker images
        run: |
          docker build -t primeai/backend:latest ./backend
          docker build -t primeai/frontend:latest ./frontend
      
      - name: Push to Docker Hub
        run: |
          echo "${{ secrets.DOCKER_PASSWORD }}" | docker login -u "${{ secrets.DOCKER_USERNAME }}" --password-stdin
          docker push primeai/backend:latest
          docker push primeai/frontend:latest
      
      - name: Deploy to production
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.PROD_HOST }}
          username: ${{ secrets.PROD_USER }}
          key: ${{ secrets.PROD_SSH_KEY }}
          script: |
            cd /app/primeai
            docker-compose pull
            docker-compose up -d
            docker-compose exec -T backend python -c "from app.database import init_db; init_db()"
```

---

## Option 2: Deploy to Cloud Providers

### AWS Deployment (Recommended for Scale)

```bash
# 1. Create EC2 instance
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --instance-type t3.medium \
  --key-name my-key \
  --security-groups default

# 2. SSH into instance
ssh -i my-key.pem ubuntu@your-ec2-ip

# 3. Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 4. Clone your repo
git clone https://github.com/YOUR-USERNAME/primeai.git
cd primeai

# 5. Configure environment
cp backend/.env.example backend/.env
# Edit backend/.env with your AWS RDS credentials

# 6. Deploy
chmod +x deploy.sh
./deploy.sh

# 7. Setup SSL with Let's Encrypt
sudo certbot certonly --standalone -d api.primeai.com -d primeai.com

# 8. Setup Nginx reverse proxy
sudo apt-get install nginx
# Configure nginx (see next section)

# 9. Enable SSL auto-renewal
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

**AWS Resources Needed:**
- EC2 (t3.medium): $30/month
- RDS PostgreSQL (db.t3.micro): $30/month
- Lambda for scheduled tasks: $1-5/month
- Route53 DNS: $0.50/month
- S3 for backups: $1/month
- Total: ~$60-70/month

### Nginx Configuration

```nginx
# /etc/nginx/sites-available/primeai

upstream backend {
  server localhost:8000;
}

server {
  listen 80;
  server_name api.primeai.com primeai.com;
  
  return 301 https://$server_name$request_uri;
}

server {
  listen 443 ssl http2;
  server_name api.primeai.com;
  
  ssl_certificate /etc/letsencrypt/live/api.primeai.com/fullchain.pem;
  ssl_certificate_key /etc/letsencrypt/live/api.primeai.com/privkey.pem;
  ssl_protocols TLSv1.2 TLSv1.3;
  ssl_ciphers HIGH:!aNULL:!MD5;
  ssl_prefer_server_ciphers on;
  
  client_max_body_size 10M;
  
  location / {
    proxy_pass http://backend;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_read_timeout 60s;
  }
}

server {
  listen 443 ssl http2;
  server_name primeai.com;
  
  ssl_certificate /etc/letsencrypt/live/primeai.com/fullchain.pem;
  ssl_certificate_key /etc/letsencrypt/live/primeai.com/privkey.pem;
  
  root /app/primeai/frontend;
  index index.html;
  
  location / {
    try_files $uri /index.html;
  }
  
  # API calls go to backend
  location /api {
    proxy_pass http://backend;
    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
  }
}
```

Enable nginx config:
```bash
sudo ln -s /etc/nginx/sites-available/primeai /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Heroku Deployment (Fastest)

```bash
# 1. Install Heroku CLI
curl https://cli.heroku.com/install.sh | sh

# 2. Login
heroku login

# 3. Create app
heroku create primeai-app

# 4. Add database addon
heroku addons:create heroku-postgresql:standard-0
heroku addons:create heroku-redis:premium-0

# 5. Set environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set STRIPE_SECRET_KEY=sk_live_your_key

# 6. Create Procfile
cat > Procfile << EOF
web: cd backend && gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
EOF

# 7. Deploy
git push heroku main

# 8. Scale
heroku ps:scale web=2
```

**Heroku Cost**: $50-200/month

### DigitalOcean Deployment

```bash
# 1. Create DigitalOcean App Platform project
doctl apps create --spec app.yaml

# 2. Create app.yaml
cat > app.yaml << 'EOF'
name: primeai
services:
- name: backend
  github:
    owner: YOUR-USERNAME
    repo: primeai
    branch: main
  build_command: pip install -r backend/requirements.txt
  run_command: cd backend && gunicorn app.main:app --workers 4
  http_port: 8000
  source_dir: backend
  
- name: frontend
  github:
    owner: YOUR-USERNAME
    repo: primeai
    branch: main
  build_command: cd frontend && npm install && npm run build
  source_dir: frontend

databases:
- name: postgres
  engine: PG
  version: "15"
  
- name: redis
  engine: REDIS
EOF

# 3. Deploy
doctl apps create --spec app.yaml
```

**DigitalOcean Cost**: $25-100/month

---

## Option 3: Manual VPS Deployment

### Step 1: Rent VPS (e.g., Linode, DigitalOcean, AWS Lightsail)

- 2GB RAM, 2 CPU: $10-15/month
- Ubuntu 22.04 LTS

### Step 2: Setup Server

```bash
# SSH into server
ssh root@your-server-ip

# Update system
apt-get update && apt-get upgrade -y

# Install dependencies
apt-get install -y \
  curl \
  wget \
  git \
  python3.11 \
  python3-pip \
  postgresql \
  postgresql-contrib \
  redis-server \
  nginx \
  certbot \
  python3-certbot-nginx

# Install Docker (recommended)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add current user to docker group
sudo usermod -aG docker $USER
```

### Step 3: Clone and Deploy

```bash
# Clone repository
git clone https://github.com/YOUR-USERNAME/primeai.git
cd primeai

# Setup environment
cp backend/.env.example backend/.env
nano backend/.env  # Edit with your config

# Run deployment script
chmod +x deploy.sh
./deploy.sh

# Verify
curl http://localhost:8000/health
```

---

## Option 4: Kubernetes (Enterprise)

```bash
# Create Kubernetes manifests
mkdir k8s

# deployment.yaml
cat > k8s/deployment.yaml << EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: primeai-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: primeai-backend
  template:
    metadata:
      labels:
        app: primeai-backend
    spec:
      containers:
      - name: backend
        image: primeai/backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: primeai-secrets
              key: database-url
        resources:
          requests:
            cpu: "250m"
            memory: "256Mi"
          limits:
            cpu: "500m"
            memory: "512Mi"
EOF

# Deploy
kubectl apply -f k8s/deployment.yaml
```

---

## Quick Comparison

| Provider | Cost | Setup Time | Scale | Best For |
|----------|------|-----------|-------|----------|
| **GitHub + AWS** | $60-200/mo | 2 hours | Excellent | Production |
| **Heroku** | $50-200/mo | 30 min | Good | MVP/Prototype |
| **DigitalOcean** | $25-100/mo | 1 hour | Good | Startups |
| **VPS Manual** | $10-50/mo | 3 hours | Fair | Bootstrap |
| **Kubernetes** | $100+/mo | 4 hours | Excellent | Enterprise |

---

## Domain Setup

### 1. Buy Domain
- Nameservers: Route53 (AWS), Cloudflare, Namecheap

### 2. Point to Server
```
api.primeai.com → Your Server IP
primeai.com → Your Server IP
```

### 3. Verify DNS
```bash
nslookup api.primeai.com
```

---

## Monitoring & Alerts

### Uptime Monitoring
```bash
# Install Prometheus + Grafana
docker run -d -p 9090:9090 prom/prometheus
docker run -d -p 3000:3000 grafana/grafana
```

### Error Tracking (Sentry)
```bash
# Add to backend/app/main.py
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn="https://YOUR-KEY@sentry.io/PROJECT-ID",
    integrations=[FastApiIntegration()]
)
```

### Simple Uptime Monitoring
```bash
# Use UptimeRobot (free tier)
# Monitor: https://api.primeai.com/health
```

---

## Next: Make Revenue

### Enable Stripe Payments

```python
# backend/app/routes/stripe.py
import stripe
from app.config import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

@router.post("/create-payment-intent")
def create_payment_intent(user_id: int, db: Session = Depends(get_db)):
    intent = stripe.PaymentIntent.create(
        amount=800,  # $8.00
        currency="usd",
        metadata={"user_id": user_id}
    )
    return {"client_secret": intent.client_secret}
```

### Setup Webhook
```python
@router.post("/webhook")
def handle_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.body()
    sig_header = request.headers.get('Stripe-Signature')
    
    event = stripe.Webhook.construct_event(
        payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
    )
    
    if event['type'] == 'payment_intent.succeeded':
        user_id = event['data']['object']['metadata']['user_id']
        create_monthly_subscription(db, user_id)
    
    return {"status": "success"}
```

---

## Checklist Before Going Live

- [ ] All environment variables configured
- [ ] SSL certificate installed
- [ ] Database backups enabled
- [ ] Email notifications working
- [ ] Monitor alerts setup
- [ ] Rate limiting tested
- [ ] Load testing completed
- [ ] Security scan passed
- [ ] Legal docs (ToS, Privacy Policy)
- [ ] Support email setup
- [ ] Payment processing tested
- [ ] Chrome extension published to Store
- [ ] Firefox extension published to Store

---

## Success Metrics

Once live, track:
```
Daily Active Users (DAU)
Monthly Active Users (MAU)
Subscription Conversion Rate (target: 20-30%)
API Call Usage (average calls/user/day)
Revenue MRR (Monthly Recurring)
Churn Rate (target: <5%/month)
```

---

## Final Step: Tell the World

```bash
# Submit to Product Hunt
# Post on HackerNews
# Email tech blogs
# Post on Reddit: r/webdev, r/startups
# Tweet about launch
# Add to BetaList / Producthunt
```

🎉 **Your PrimeAI is now LIVE!**
