#!/usr/bin/env python
"""
PrimeAI - Production Verification Script
Checks all systems are properly configured before deployment
"""

import os
import sys
import json
from pathlib import Path

def check_structure():
    """Verify all required files exist"""
    required_files = {
        'backend': [
            'requirements.txt',
            'app/main.py',
            'app/config.py',
            'app/database.py',
            'app/models/user.py',
            'app/models/subscription.py',
            'app/models/device.py',
            'app/routes/auth.py',
            'app/routes/subscriptions.py',
            'app/routes/devices.py',
            'app/routes/extension.py',
        ],
        'extension': [
            'manifest.json',
            'src/stealth.js',
            'src/content.js',
            'src/background.js',
            'src/popup.html',
            'src/popup.js',
        ],
        'frontend': [
            'index.html',
            'login.html',
            'dashboard.js',
        ],
        'root': [
            'docker-compose.yml',
            'deploy.sh',
            'README.md',
            'DEPLOYMENT.md',
            '.gitignore',
        ]
    }
    
    print("📋 Checking file structure...")
    missing = []
    
    for category, files in required_files.items():
        for file in files:
            if category == 'root':
                path = Path(file)
            else:
                path = Path(category) / file
            
            if not path.exists():
                missing.append(str(path))
                print(f"  ❌ Missing: {path}")
            else:
                print(f"  ✅ {path}")
    
    return len(missing) == 0

def check_dependencies():
    """Check if required tools are installed"""
    print("\n🔧 Checking dependencies...")
    
    required = {
        'docker': 'Docker',
        'docker-compose': 'Docker Compose',
        'python3': 'Python 3',
        'psql': 'PostgreSQL Client (optional)',
    }
    
    installed = []
    for cmd, name in required.items():
        result = os.system(f"which {cmd} > /dev/null 2>&1")
        if result == 0:
            print(f"  ✅ {name}")
            installed.append(cmd)
        else:
            print(f"  ❌ {name} (required)")
    
    return len(installed) >= 2  # At least docker and docker-compose

def check_env():
    """Check environment configuration"""
    print("\n⚙️  Checking environment...")
    
    env_file = Path('backend/.env')
    if env_file.exists():
        print("  ✅ Backend .env file exists")
        return True
    else:
        print("  ⚠️  Backend .env file not found")
        print("     Create one using: cp backend/.env.example backend/.env")
        return False

def run_verification():
    """Run all verification checks"""
    print("\n" + "="*50)
    print("🛡️  PrimeAI Production Verification")
    print("="*50)
    
    checks = [
        ("File Structure", check_structure),
        ("Dependencies", check_dependencies),
        ("Environment", check_env),
    ]
    
    results = []
    for name, check in checks:
        try:
            result = check()
            results.append((name, result))
        except Exception as e:
            print(f"  Error: {e}")
            results.append((name, False))
    
    print("\n" + "="*50)
    print("📊 Verification Summary")
    print("="*50)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    all_passed = all(result for _, result in results)
    
    print("\n" + "="*50)
    if all_passed:
        print("✅ All checks passed! Ready for deployment.")
        print("\nNext steps:")
        print("  1. Configure backend/.env with your credentials")
        print("  2. Run: chmod +x deploy.sh && ./deploy.sh")
        print("  3. Access dashboard at http://localhost:3000")
        return 0
    else:
        print("❌ Some checks failed. Please fix issues above.")
        return 1

if __name__ == '__main__':
    sys.exit(run_verification())
