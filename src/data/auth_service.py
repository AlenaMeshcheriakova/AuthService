import datetime
import uuid
from typing import Optional
from pydantic import BaseModel
from cfg.сonfig import settings
from src.db.database import session_factory
from src.log.logger import log_decorator, CustomLogger
from src.model.userdb import UserDB
from jose import JWTError, jwt

class TokenData(BaseModel):
    username: Optional[str] = None

class AuthOrm:

    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def get_user_by_email(email: str):
        """
        Get user from the database using their email
        :param email: email
        :return: User
        """
        with session_factory() as session:
            return session.query(UserDB).filter(UserDB.email == email).first()

    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def get_user_by_username(username: str):
        """
        Get user from the database using their username
        :param username: username
        :return: User
        """
        with session_factory() as session:
            return session.query(UserDB).filter(UserDB.user_name == username).first()

    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def create_user(email: str, password: str, username: str, telegram_user_id:str) -> UserDB:
        """
        Method for creating AUTH user
        :param email:email
        :param password:password
        :param username:username
        :param telegram_user_id:telegram_user_id
        :return:UserDB object
        """
        with session_factory() as session:
            new_user = UserDB(
                id=uuid.uuid4(),
                email=email,
                password=password,
                user_name=username,
                telegram_user_id=telegram_user_id
            )
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
            return new_user

    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def create_access_token(data: dict, expires_delta: Optional[datetime.timedelta] = None):
        """
        Creates a JWT access token with an expiration time
        :param data: data information
        :param expires_delta: expires_delta
        :return: JWT token
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.datetime.utcnow() + expires_delta
        else:
            expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt

    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def verify_token(token: str) -> TokenData:
        """
        Verify a JWT token. Decode JWT token and extract username, otherwise raise an exception
        :param token:JWT
        :return: TokenData with username
        """
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise JWTError("Invalid token")
            token_data = TokenData(username=username)
            return token_data
        except JWTError:
            raise JWTError("Token verification failed")