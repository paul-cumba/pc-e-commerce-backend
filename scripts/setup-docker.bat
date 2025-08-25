@echo off
REM E-commerce API Docker Setup Script for Windows
echo 🐳 Setting up Docker PostgreSQL for E-commerce API...

REM Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not running. Please start Docker Desktop and try again.
    pause
    exit /b 1
)

REM Start PostgreSQL with Docker Compose
echo 📦 Starting PostgreSQL container...
docker-compose up -d postgres

REM Wait for PostgreSQL to be ready
echo ⏳ Waiting for PostgreSQL to be ready...
set timeout=30
set counter=0

:wait_loop
if %counter% geq %timeout% (
    echo ❌ PostgreSQL failed to start within %timeout% seconds
    echo 📋 Check logs with: docker-compose logs postgres
    pause
    exit /b 1
)

docker-compose exec -T postgres pg_isready -U ecommerce_user -d ecommerce_db >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ PostgreSQL is ready!
    goto :db_ready
)

echo    Still waiting... (%counter%/%timeout%)
timeout /t 2 /nobreak >nul
set /a counter+=2
goto :wait_loop

:db_ready
REM Initialize database tables
echo 🗄️  Initializing database tables...
python -m app.db.init_db
if %errorlevel% equ 0 (
    echo ✅ Database tables created successfully!
) else (
    echo ❌ Failed to create database tables
    pause
    exit /b 1
)

echo.
echo 🎉 Setup complete! Your PostgreSQL database is ready.
echo.
echo 📊 Database Info:
echo    Host: localhost
echo    Port: 5432
echo    Database: ecommerce_db
echo    User: ecommerce_user
echo.
echo 🚀 Next steps:
echo    1. Start your API: python run.py
echo    2. Visit API docs: http://localhost:8000/docs
echo    3. Optional - Start pgAdmin: docker-compose --profile tools up -d pgadmin
echo       Then visit: http://localhost:8080 (admin@ecommerce.com / admin123)
echo.
echo 🛠️  Useful commands:
echo    Stop database: docker-compose down
echo    View logs: docker-compose logs postgres
echo    Connect to DB: docker-compose exec postgres psql -U ecommerce_user -d ecommerce_db
echo.
pause
