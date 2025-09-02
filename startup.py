#!/usr/bin/env python3
"""
Startup script for the Cover Letter Writer Bot
This script helps debug startup issues and ensures proper initialization
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_environment():
    """Check if all required environment variables are set"""
    required_vars = ['MONGO_URI', 'PORT']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        return False
    
    print("✅ All required environment variables are set")
    return True

def check_database():
    """Test database connection"""
    try:
        from database import client
        client.admin.command('ping')
        print("✅ Database connection successful")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def main():
    """Main startup function"""
    print("🚀 Starting Cover Letter Writer Bot...")
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Check database
    if not check_database():
        print("⚠️  Database connection failed, but continuing...")
    
    # Import and start Flask app
    try:
        from app import app, PORT
        print(f"✅ Flask app imported successfully")
        print(f"🌐 Starting server on port {PORT}")
        app.run(host="0.0.0.0", port=PORT, debug=False)
    except Exception as e:
        print(f"❌ Failed to start Flask app: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
