# PrimeAI - Interview Shield
# Production-Ready Anti-Detect Browser Extension

## Features

✅ **Completely Undetectable**
- Browser fingerprint spoofing
- Canvas & WebGL fingerprinting prevention
- WebRTC leak prevention
- DevTools detection bypass
- User agent randomization

✅ **Interview-Optimized**
- Interview Mode with maximum stealth
- Simulates realistic user behavior
- Keyboard & mouse movement randomization
- Timezone & language spoofing
- Prevents detection by HireVue, Proctorio, and other platforms

✅ **Production-Ready**
- FastAPI backend with PostgreSQL
- JWT authentication
- Subscription management
- API rate limiting (1000 calls/month)
- Cloud-ready Docker deployment

✅ **Cross-Platform**
- Chrome/Chromium extension
- Firefox support
- Mobile-friendly dashboard
- Responsive UI

## Installation

### Prerequisites
- Docker & Docker Compose
- Node.js 18+
- Python 3.11+
- PostgreSQL 15+

### Quick Start

```bash
# Make deploy script executable
chmod +x deploy.sh

# Run deployment
./deploy.sh
```

### Manual Setup

```bash
# Backend setup
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your credentials
python run.py

# Frontend setup
cd frontend
npm install
npm run dev

# Docker setup
docker-compose up -d
```

## Configuration

### Backend (.env)
```env
DATABASE_URL=postgresql://user:password@localhost:5432/primeai_db
SECRET_KEY=your-secret-key-min-32-chars
STRIPE_SECRET_KEY=sk_live_your_key
API_URL=https://api.primeai.com
FRONTEND_URL=https://primeai.com
```

### Extension Setup
1. Clone or download the extension folder
2. Open `chrome://extensions/` in Chrome
3. Enable "Developer mode" (top right)
4. Click "Load unpacked" and select the `extension` folder
5. Login with your PrimeAI account

## Pricing

- **1-Day Free Trial**: Included with signup
- **Monthly Plan**: $8 USD (~1,000 KES)
  - Unlimited device profiles
  - 1,000 API calls/month
  - All anti-detect features
  - Interview mode access

## API Endpoints

### Authentication
```
POST   /api/auth/register     Create account
POST   /api/auth/login        Login
GET    /api/auth/me           Get current user
```

### Device Profiles
```
POST   /api/devices/create    Create profile
GET    /api/devices/list      List all profiles
GET    /api/devices/{id}      Get profile details
PUT    /api/devices/{id}      Update profile
DELETE /api/devices/{id}      Delete profile
```

### Anti-Detect
```
POST   /api/extension/config      Get extension config
POST   /api/extension/validate    Validate subscription
```

### Subscriptions
```
GET    /api/subscriptions/active  Get active subscription
GET    /api/subscriptions/list    List all subscriptions
POST   /api/subscriptions/cancel  Cancel subscription
```

## Security Features

🔒 **Maximum Security**
- End-to-end encryption for sensitive data
- JWT token-based authentication
- CORS protection enabled
- SQL injection prevention
- XSS protection
- CSRF protection
- Rate limiting on all endpoints
- IP whitelisting support

🛡️ **Anti-Detection**
- Hides all extension traces
- Blocks DevTools detection
- Disables right-click inspection
- Randomizes timing patterns
- Spoofs device capabilities
- Prevents fingerprinting databases

## Database Schema

### Users Table
- id, email, username, hashed_password
- is_active, is_verified
- created_at, updated_at

### Subscriptions Table
- id, user_id, plan_type
- start_date, end_date, trial_end_date
- api_calls_used, api_calls_limit
- stripe_subscription_id, stripe_customer_id

### Device Profiles Table
- id, user_id, profile_name
- user_agent, platform, device_model
- screen dimensions, timezone, language
- Anti-detect settings (canvas_noise, webgl_noise, etc)
- interview_mode flag

## Browser Extension Architecture

### manifest.json
- Defined permissions and content scripts
- UI popup configuration
- Web-accessible resources

### stealth.js
- Core anti-detect library
- Runs in isolated world
- Injects fingerprint spoofing
- Handles canvas/WebGL randomization

### content.js
- Page injection handler
- Communication bridge
- Subscription validation

### background.js (Service Worker)
- Profile management
- API communication
- Configuration broadcasting
- Subscription checking

## Deployment

### Docker Production

```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# Initialize database
docker-compose exec backend python -c "from app.database import init_db; init_db()"

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Kubernetes (Optional)

Create deployment files for production Kubernetes clusters:

```yaml
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
```

### Environment Scaling

For production with 100K+ concurrent users:
1. Use AWS RDS for PostgreSQL
2. Use ElastiCache for Redis
3. Use ALB (Application Load Balancer)
4. CDN for frontend (CloudFront)
5. WAF (Web Application Firewall)

## Traffic Estimation

With pricing model:
- **$8/month** per paying user
- **1,000 API calls/month** per user
- **1-day free trial** (~20% conversion)

At scale:
- 10,000 paying users = $80,000/month revenue
- 50,000 API calls daily = 1.5M calls/month

## Support & Documentation

- 📧 Email: support@primeai.com
- 💬 Discord: [Join Community]
- 📖 Docs: https://docs.primeai.com
- 🐛 Issues: GitHub Issues

## License

MIT License - See LICENSE file

## Disclaimer

This tool is for educational and authorized use only. Users are responsible for complying with:
- Platform terms of service
- Local laws and regulations
- Employer policies
- Ethical guidelines

Unauthorized access or circumventing security measures is illegal.

## Future Roadmap

- [ ] Advanced ML-based behavior patterns
- [ ] Blockchain-based verification
- [ ] AI-powered natural language patterns
- [ ] Real-time threat detection
- [ ] Custom interview profiles
- [ ] Team collaboration features
- [ ] Mobile app (iOS/Android)
- [ ] Enterprise pricing tier

---

Built with ❤️ by the PrimeAI Team
