from werkzeug.security import generate_password_hash

hashed_password = generate_password_hash("marcusjoto")

print(hashed_password)