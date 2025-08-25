"""
Database initialization script
"""
from app.db.database import engine
from app.db import models


def create_tables():
    """Create all database tables"""
    models.Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")


if __name__ == "__main__":
    create_tables()
