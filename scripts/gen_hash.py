import hashlib

def generate_md5(user_login, user_pass):
    # Concatenate username and password
    data = user_login.encode() + user_pass.encode()

    # Create MD5 hash
    user_md5_hash = hashlib.md5(data).hexdigest()

    return user_md5_hash

