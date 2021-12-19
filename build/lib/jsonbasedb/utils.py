from hashlib import pbkdf2_hmac

def return_hash(text, salt):
  return pbkdf2_hmac('sha256', text.encode('utf-8'), salt.encode('utf-8'), 100000).hex()
