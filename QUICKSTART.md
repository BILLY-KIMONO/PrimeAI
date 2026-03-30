# PrimeAI - Production Setup Guide

## Quick Commands

```bash
# Make scripts executable
chmod +x deploy.sh

# Deploy to production
./deploy.sh

# Manual backends start
cd backend && pip install -r requirements.txt && python run.py

# Manual frontend start
cd frontend && npm install && npm run dev

# Docker compose
docker-compose up -d
docker-compose logs -f
docker-compose down

# Access services
# Backend API: http://localhost:8000
# Frontend: http://localhost:3000
# API Docs: http://localhost:8000/docs
```

## System Requirements

- CPU: 2+ cores (t3.small on AWS)
- RAM: 4GB minimum (8GB recommended)
- Storage: 50GB SSD
- OS: Ubuntu 22.04 LTS
- Bandwidth: 100 Mbps+

## Important Notes

1. **Change all default credentials** in .env before production
2. **Enable HTTPS** using Let's Encrypt on production
3. **Setup daily database backups**
4. **Configure CDN** for static assets
5. **Enable monitoring** (Sentry, DataDog, etc)
6. **Setup email provider** for user notifications
7. **Configure Stripe** for payment processing

## Troubleshooting

### Extension not loading?
- Check browser console for errors
- Verify API URL in extension settings
- Clear extension cache and reload

### API connection failed?
- Verify backend is running: `curl http://localhost:8000/health`
- Check CORS settings in backend
- Review firewall rules

### Database migrations failing?
- Ensure PostgreSQL is running
- Check DATABASE_URL in .env
- Run: `python -c "from app.database import init_db; init_db()"`

## Support

For issues, email: support@primeai.com
