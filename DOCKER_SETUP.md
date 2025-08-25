# Docker PostgreSQL Setup Guide

This guide walks you through setting up PostgreSQL using Docker for the E-commerce API.

## Quick Start

### 1. Prerequisites
- Docker Desktop installed and running
- Python 3.8+ with dependencies installed (`pip install -r requirements.txt`)

### 2. Automated Setup (Recommended)

**On macOS/Linux:**
```bash
./scripts/setup-docker.sh
```

**On Windows:**
```bash
scripts\setup-docker.bat
```

### 3. Manual Setup

**Start PostgreSQL:**
```bash
docker-compose up -d postgres
```

**Wait for PostgreSQL to be ready:**
```bash
# Check if PostgreSQL is ready
docker-compose exec postgres pg_isready -U ecommerce_user -d ecommerce_db
```

**Initialize database tables:**
```bash
python -m app.db.init_db
```

## Database Connection Details

- **Host:** localhost
- **Port:** 5432
- **Database:** ecommerce_db
- **Username:** ecommerce_user
- **Password:** secure_password_123

## Useful Docker Commands

### Container Management
```bash
# Start PostgreSQL
docker-compose up -d postgres

# Stop PostgreSQL
docker-compose down

# Restart PostgreSQL
docker-compose restart postgres

# View container status
docker-compose ps

# View PostgreSQL logs
docker-compose logs postgres

# Follow PostgreSQL logs in real-time
docker-compose logs -f postgres
```

### Database Access
```bash
# Connect to PostgreSQL using psql
docker-compose exec postgres psql -U ecommerce_user -d ecommerce_db

# Run SQL commands directly
docker-compose exec postgres psql -U ecommerce_user -d ecommerce_db -c "SELECT version();"

# Create a database backup
docker-compose exec postgres pg_dump -U ecommerce_user ecommerce_db > backup.sql

# Restore from backup
docker-compose exec -T postgres psql -U ecommerce_user -d ecommerce_db < backup.sql
```

### Optional: pgAdmin (Database Management UI)
```bash
# Start pgAdmin along with PostgreSQL
docker-compose --profile tools up -d

# Access pgAdmin at: http://localhost:8080
# Login: admin@ecommerce.com
# Password: admin123
```

## Troubleshooting

### Container Won't Start
```bash
# Check if port 5432 is already in use
lsof -i :5432

# Remove existing container and start fresh
docker rm -f ecommerce-postgres
docker-compose up -d postgres
```

### Connection Issues
```bash
# Verify container is running
docker ps | grep postgres

# Check container logs for errors
docker-compose logs postgres

# Test connection
docker-compose exec postgres pg_isready -U ecommerce_user -d ecommerce_db
```

### Data Persistence
The PostgreSQL data is stored in a Docker volume named `pc-e-commerce-backend_postgres_data`. This ensures your data persists even if you remove and recreate the container.

```bash
# List Docker volumes
docker volume ls

# Inspect the PostgreSQL volume
docker volume inspect pc-e-commerce-backend_postgres_data

# Remove volume (WARNING: This will delete all data)
docker volume rm pc-e-commerce-backend_postgres_data
```

## Production Considerations

### Security
1. Change the default password in `docker-compose.yml`
2. Use environment variables for sensitive data
3. Restrict network access to the database
4. Enable SSL/TLS connections

### Performance
1. Adjust PostgreSQL configuration for your workload
2. Set up connection pooling
3. Configure appropriate resource limits
4. Monitor database performance

### Backup Strategy
1. Set up automated backups
2. Test backup restoration procedures
3. Store backups in a secure location
4. Document recovery procedures

## Environment Variables

You can override default values using environment variables:

```bash
# Example: Change database password
export POSTGRES_PASSWORD=your_secure_password
docker-compose up -d postgres
```

Common environment variables:
- `POSTGRES_DB`: Database name (default: ecommerce_db)
- `POSTGRES_USER`: Database user (default: ecommerce_user)
- `POSTGRES_PASSWORD`: Database password (default: secure_password_123)
- `POSTGRES_PORT`: Database port (default: 5432)

## Next Steps

After setting up PostgreSQL:

1. **Start your API:**
   ```bash
   python run.py
   ```

2. **Access API documentation:**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

3. **Run tests:**
   ```bash
   pytest
   ```

4. **Test API endpoints:**
   ```bash
   # Health check
   curl http://localhost:8000/health
   
   # Get all products
   curl http://localhost:8000/api/v1/products/
