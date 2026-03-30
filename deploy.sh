#!/bin/bash

# PrimeAI Production Deployment Script

set -e

echo "🛡️  PrimeAI - Interview Shield Production Setup"
echo "================================================"

# Check dependencies
if ! command -v docker &> /dev/null; then
  echo "❌ Docker is not installed. Please install Docker first."
  exit 1
fi

if ! command -v docker-compose &> /dev/null; then
  echo "❌ Docker Compose is not installed. Please install Docker Compose first."
  exit 1
fi

# Generate secrets
echo "🔐 Generating secrets..."
SECRET_KEY=$(openssl rand -hex 32)
DB_PASSWORD=$(openssl rand -hex 16)

# Create .env file
echo "📝 Creating .env file..."
cat > backend/.env << EOF
DATABASE_URL=postgresql://primeai_user:${DB_PASSWORD}@postgres:5432/primeai_db
REDIS_URL=redis://redis:6379
SECRET_KEY=${SECRET_KEY}
ENV=production
DEBUG=False
API_URL=https://api.primeai.com
FRONTEND_URL=https://primeai.com
STRIPE_SECRET_KEY=${STRIPE_SECRET_KEY:-sk_test_your_key}
STRIPE_PUBLISHABLE_KEY=${STRIPE_PUBLISHABLE_KEY:-pk_test_your_key}
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=${SMTP_USER:-your-email@gmail.com}
SMTP_PASSWORD=${SMTP_PASSWORD:-your-app-password}
EOF

echo "✅ Environment file created"

# Build and start containers
echo "🚀 Building and starting services..."
docker-compose up -d

echo "⏳ Waiting for services to be ready..."
sleep 10

# Initialize database
echo "🗄️  Initializing database..."
docker-compose exec -T backend python -c "from app.database import init_db; init_db()"

echo ""
echo "✅ PrimeAI is now running!"
echo ""
echo "📊 Service URLs:"
echo "   Backend API: http://localhost:8000"
echo "   Frontend:    http://localhost:3000"
echo "   Health:      http://localhost:8000/health"
echo ""
echo "🔐 Database credentials:"
echo "   User: primeai_user"
echo "   Password: (check .env file)"
echo ""
echo "📚 Documentation:"
echo "   API Docs:    http://localhost:8000/docs"
echo "   ReDoc:       http://localhost:8000/redoc"
echo ""
echo "🛑 To stop services: docker-compose down"
echo "📊 To view logs: docker-compose logs -f"
