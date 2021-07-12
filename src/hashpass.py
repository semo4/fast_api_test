from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash():
    def hashing_pass(password: str):
        return pwd_context.hash(password)

    def verify(stored_password, passed_password):
        return pwd_context.verify(passed_password, stored_password)
