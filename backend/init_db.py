#!/usr/bin/env python3
"""
Database initialization script
Creates all tables including the new Payment table
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine
from app.config import settings
from app.models.base import Base
from app.models import User, Subscription, DeviceProfile, Payment

def init_db():
    """Initialize database with all tables"""
    engine = create_engine(settings.DATABASE_URL)
    
    print("🔍 Creating database tables...")
    Base.metadata.create_all(engine)
    
    print("✅ Database initialized successfully!")
    print("\nTables created:")
    print("  - users")
    print("  - subscriptions")
    print("  - device_profiles")
    print("  - payments")
    
    # Verify tables exist
    from sqlalchemy import inspect
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    required_tables = ["users", "subscriptions", "device_profiles", "payments"]
    missing_tables = [t for t in required_tables if t not in tables]
    
    if missing_tables:
        print(f"\n⚠️  Warning: Missing tables: {', '.join(missing_tables)}")
        return False
    
    print("\n✅ All required tables exist!")
    return True

if __name__ == "__main__":
    try:
        success = init_db()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)
