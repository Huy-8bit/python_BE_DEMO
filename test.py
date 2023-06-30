# from datetime import datetime

# __import__("os").environ["TZ"] = "UTC"


# print(datetime.now().timestamp())

import hashlib


def hash_password(password):
    # Create a new SHA3_256 hash object
    hash_object = hashlib.sha3_256()

    # Hash the password by encoding it as UTF-8 and updating the hash object
    hash_object.update(password.encode("utf-8"))

    # Get the hexadecimal representation of the hash
    hashed_password = hash_object.hexdigest()

    return hashed_password


# Example usage
password = "my_password"
hashed_password = hash_password(password)
print("Hashed password:", hashed_password)
