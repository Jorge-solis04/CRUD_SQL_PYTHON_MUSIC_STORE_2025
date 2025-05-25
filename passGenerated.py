from werkzeug.security import generate_password_hash

hashed_password = generate_password_hash("jorge0520")

print(hashed_password)