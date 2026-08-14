import random
import bcrypt

def generate_otp() -> str:
    return str(random.randint(100000, 999999))

def hash_otp(otp: str) -> str:
    # Use minimum rounds (4) since OTPs are short-lived and we need to return fast
    salt = bcrypt.gensalt(rounds=4)
    hashed = bcrypt.hashpw(otp.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_otp_hash(plain_otp: str, hashed_otp: str) -> bool:
    try:
        return bcrypt.checkpw(plain_otp.encode('utf-8'), hashed_otp.encode('utf-8'))
    except Exception:
        return False
