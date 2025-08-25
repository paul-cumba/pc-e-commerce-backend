#!/bin/bash

# E-commerce API Docker Setup Script
echo "🐳 Setting up Docker PostgreSQL for E-commerce API..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop and try again."
    exit 1
fi

# Start PostgreSQL with Docker Compose
echo "📦 Starting PostgreSQL container..."
docker-compose up -d postgres

# Wait for PostgreSQL to be ready
echo "⏳ Waiting for PostgreSQL to be ready..."
timeout=30
counter=0

while [ $counter -lt $timeout ]; do
    if docker-compose exec -T postgres pg_isready -U ecommerce_user -d ecommerce_db > /dev/null 2>&1; then
        echo "✅ PostgreSQL is ready!"
        break
    fi
    
    echo "   Still waiting... ($counter/$timeout)"
    sleep 2
    counter=$((counter + 2))
done

if [ $counter -ge $timeout ]; then
    echo "❌ PostgreSQL failed to start within $timeout seconds"
    echo "📋 Check logs with: docker-compose logs postgres"
    exit 1
fi

# Initialize database tables
echo "🗄️  Initializing database tables..."
if python -m app.db.init_db; then
    echo "✅ Database tables created successfully!"
else
    echo "❌ Failed to create database tables"
    exit 1
fi

echo ""
echo "🎉 Setup complete! Your PostgreSQL database is ready."
echo ""
echo "📊 Database Info:"
echo "   Host: localhost"
echo "   Port: 5432"
echo "   Database: ecommerce_db"
echo "   User: ecommerce_user"
echo ""
echo "🚀 Next steps:"
echo "   1. Start your API: python run.py"
echo "   2. Visit API docs: http://localhost:8000/docs"
echo "   3. Optional - Start pgAdmin: docker-compose --profile tools up -d pgadmin"
echo "      Then visit: http://localhost:8080 (admin@ecommerce.com / admin123)"
echo ""
echo "🛠️  Useful commands:"
echo "   Stop database: docker-compose down"
echo "   View logs: docker-compose logs postgres"
echo "   Connect to DB: docker-compose exec postgres psql -U ecommerce_user -d ecommerce_db"
