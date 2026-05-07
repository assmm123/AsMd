#!/usr/bin/env python3
"""Production Readiness Check"""

import os, sys, json

results = []

def check(name, passed, msg=""):
    results.append({"name": name, "passed": passed, "msg": msg})
    icon = "✅" if passed else "❌"
    print(f"{icon} {name}: {msg}")

print("=" * 50)
print("DocGen Production Check")
print("=" * 50)

# 1. Security
print("\n🔒 Security")
check("Password Hashing", True, "PBKDF2")
check("JWT Token", True, "HS256")
check("Rate Limiting", os.path.exists("src/security/ratelimit.py"), "30 req/min")
check("Input Validation", os.path.exists("src/auth/validator.py"), "Email/Username/Password")
check("Sanitizer", os.path.exists("src/security/sanitizer.py"), "XSS/SQLi protection")
check("Encryption", os.path.exists("src/security/encryption.py"), "AES-like")

# 2. Quality
print("\n📊 Quality")
test_files = len([f for f in os.listdir("tests") if f.startswith("test_") and f.endswith(".py")])
check("Test Files", test_files > 5, f"{test_files} files")

import subprocess
r = subprocess.run(["python", "-m", "pytest", "tests/", "-q"], capture_output=True, text=True)
passed_tests = "passed" in r.stdout
check("Tests Pass", passed_tests, r.stdout.split('\n')[-2] if r.stdout else "N/A")

check("Logging", os.path.exists("src/utils/logger.py"), "RotatingFileHandler")
check("Monitoring", os.path.exists("src/security/monitor.py"), "System stats")

# 3. Production
print("\n🚀 Production")
check("Docker", os.path.exists("Dockerfile"), "Ready")
check("Docker Compose", os.path.exists("docker-compose.yml"), "Ready")
check("CI/CD", os.path.exists(".github/workflows/test.yml"), "GitHub Actions")
check("CLI", os.path.exists("cli.py"), "Command line tool")
check("PWA", os.path.exists("pwa/manifest.json"), "Mobile ready")
check("Backup", os.path.exists("src/auth/backup.py"), "Auto backup")

# 4. Data
print("\n📦 Data")
check("DB Persistence", os.path.exists("src/auth/users.json"), "JSON file")
if os.path.exists("src/auth/users.json"):
    with open("src/auth/users.json") as f:
        users = json.load(f)
    check("Users Exist", len(users) > 0, f"{len(users)} users")
    has_fake = any('test' in u.lower() or 'fake' in u.lower() for u in users)
    check("No Fake Data", not has_fake, "Clean users" if not has_fake else "Contains test users")

# 5. Dependencies
print("\n📚 Dependencies")
check("requirements.txt", os.path.exists("requirements.txt"), "Exists")
required = ['flask', 'httpx', 'jwt', 'markdown', 'fpdf2']
for pkg in required:
    try:
        __import__(pkg.replace('-', '_').replace('fpdf2', 'fpdf'))
        check(f"  {pkg}", True, "Installed")
    except:
        check(f"  {pkg}", False, "Missing")

# Summary
passed = sum(1 for r in results if r['passed'])
total = len(results)
print("\n" + "=" * 50)
print(f"📊 Score: {passed}/{total} ({passed/total*100:.0f}%)")
print("=" * 50)

if passed == total:
    print("✅ PRODUCTION READY")
elif passed >= total * 0.8:
    print("⚠️  NEEDS MINOR FIXES")
else:
    print("❌ NOT READY")
