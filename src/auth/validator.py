import re

def validate_username(username):
    if not username or len(username) < 3:
        return False, "Username must be at least 3 characters"
    if len(username) > 30:
        return False, "Username must be less than 30 characters"
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "Username: letters, numbers, underscore only"
    return True, ""

def validate_email(email):
    if not email:
        return True, ""  # Email optional
    if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
        return False, "Invalid email format"
    return True, ""

def validate_password(password):
    if not password or len(password) < 3:
        return False, "Password must be at least 3 characters"
    if len(password) > 100:
        return False, "Password too long"
    return True, ""
