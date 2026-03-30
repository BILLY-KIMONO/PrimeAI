#!/bin/bash

# Production deployment guidelines

## Pre-Deployment Checklist

- [ ] All environment variables configured
- [ ] SSL certificates generated
- [ ] Database backups enabled
- [ ] Redis persistence configured
- [ ] Monitoring & logging setup
- [ ] Security scan completed
- [ ] Load testing passed
- [ ] Backup & recovery tested

## Deployment Steps

### 1. Server Setup
- Provision Ubuntu 22.04 instance
- Install Docker, Docker Compose, nginx
- Configure firewall (allow 80, 443, 22)

### 2. SSL/TLS
```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Generate certificate
sudo certbot certonly --nginx -d primeai.com -d api.primeai.com
```

### 3. Nginx Configuration
```nginx
upstream backend {
  server backend:8000;
}

server {
  listen 443 ssl http2;
  server_name api.primeai.com;
  
  ssl_certificate /etc/letsencrypt/live/api.primeai.com/fullchain.pem;
  ssl_certificate_key /etc/letsencrypt/live/api.primeai.com/privkey.pem;
  
  location / {
    proxy_pass http://backend;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
  }
}
```

### 4. Database Backup
```bash
# Daily backups
0 2 * * * docker-compose exec -T postgres pg_dump -U primeai_user primeai_db > /backups/db_$(date +\%Y\%m\%d).sql
```

### 5. Monitoring
- Set up uptime monitoring (UptimeRobot)
- Error tracking (Sentry)
- Performance monitoring (New Relic)
- Log aggregation (ELK stack)

### 6. Security
- Enable rate limiting
- DDoS protection (Cloudflare)
- Web Application Firewall
- Regular security audits

## Scaling Strategy

### Horizontal Scaling (Multiple Servers)

1. **Load Balancer**: AWS ALB or nginx
2. **Backend Servers**: 3+ instances
3. **Database**: AWS RDS with Multi-AZ
4. **Cache**: AWS ElastiCache Redis Cluster
5. **CDN**: CloudFront for static assets

### Vertical Scaling (Increase Resources)

- Increase CPU/RAM if usage > 70%
- Use connection pooling (pgBouncer)
- Enable Redis persistence
- Optimize database queries

## Monitoring & Alerts

### Key Metrics
- API response time (target: <200ms)
- Error rate (target: <0.1%)
- CPU usage (alert at 80%)
- Memory usage (alert at 85%)
- Database connections (alert at 80% limit)
- Redis RAM usage (alert at 90%)

### Alerting
```bash
# Configure alerts in monitoring tool
- 5xx errors > 10 in 5min -> page
- Response time > 1s for 10min -> email
- Disk usage > 90% -> email
- Database down -> page
```

## Rollback Procedure

```bash
# Save current version
docker-compose images > deployed_version.txt

# Rollback
docker-compose down
git checkout previous_tag
docker-compose up -d
docker-compose exec backend python -c "from app.database import init_db; init_db()"
```

## Cost Estimation

### Monthly Costs (100K users)
- Compute (3x m5.large): $300
- RDS PostgreSQL (db.r5.large): $400
- ElastiCache Redis (cache.r6g.large): $200
- Bandwidth: $500
- CDN: $100
- Monitoring tools: $300
- **Total: ~$1,800/month**

### Revenue at Scale
- $8/user × 10,000 paying users = $80,000/month
- **Profit margin: ~95%** (after ops & support)

## CI/CD Pipeline

```yaml
# GitHub Actions example
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build & push Docker images
        run: |
          docker login -u ${{ secrets.DOCKER_USER }} -p ${{ secrets.DOCKER_PASS }}
          docker-compose build
          docker-compose push
      - name: Deploy to production
        run: |
          ssh deploy@prod-server 'cd /app && docker-compose pull && docker-compose up -d'
```

## Compliance & Legal

- ✅ GDPR compliance (user data privacy)
- ✅ Data retention policies
- ✅ Terms of Service & Privacy Policy
- ✅ Regular security audits
- ✅ Incident response plan

---

For more info: support@primeai.com
