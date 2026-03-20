from app.core.security import hash_password

password = "Admin123!"
print(hash_password(password))