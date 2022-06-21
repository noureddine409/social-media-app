
from passlib.context import CryptContext

pwdContext = CryptContext(schemes=['bcrypt'], deprecated= 'auto')

def hash(password: str):
    return pwdContext.hash(password)

def verify(loginPassword, hashedPassword):
    return pwdContext.verify(loginPassword, hashedPassword)