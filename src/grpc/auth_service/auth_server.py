import datetime

import grpc
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError

from cfg.сonfig import settings
from src.grpc.auth_service import auth_service_pb2
from src.grpc.auth_service.auth_service_pb2_grpc import AuthService
from src.data.auth_service import AuthOrm


class AuthServiceServicer(AuthService):

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def login(self, request: auth_service_pb2.LoginRequest, context: grpc.ServicerContext) -> (
            auth_service_pb2.LoginResponse):
        # Get user from DB
        user = AuthOrm.get_user_by_username(request.username)

        # Check that user exist and verify
        if not user or not self.pwd_context.verify(request.password, user.hashed_password):
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details("Invalid credentials")
            return auth_service_pb2.LoginResponse()

        # Create token
        expires_delta = datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        data = {"sub": user.user_name}
        access_token = AuthOrm.create_access_token(data, expires_delta)

        return auth_service_pb2.LoginResponse(token=access_token,
                                              expires_in=str(settings.ACCESS_TOKEN_EXPIRE_MINUTES))

    def validate_token(self, request: auth_service_pb2.ValidateTokenRequest,
                      context: grpc.ServicerContext) -> auth_service_pb2.ValidateTokenResponse:
        try:
            payload = jwt.decode(request.token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise JWTError("Invalid token")

            # Get user from DB
            user = AuthOrm.get_user_by_username(username)

            if user is None:
                raise JWTError("User not found")

            # Create response
            return auth_service_pb2.ValidateTokenResponse(
                is_valid=True,
                user_id=str(user.id),
                email=user.email,
                username=user.user_name
            )
        except JWTError:
            return auth_service_pb2.ValidateTokenResponse(is_valid=False)

    def register(self, request: auth_service_pb2.RegisterRequest, context: grpc.ServicerContext) -> (
            auth_service_pb2.RegisterResponse):
        try:
            # Create Auth User
            user = AuthOrm.create_user(
                request.email,
                request.password,
                request.username,
                request.telegram_user_id
            )
            return auth_service_pb2.RegisterResponse(
                username=user.user_name,
                message="User registered successfully"
            )
        except IntegrityError:
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            context.set_details("User already exists")
            return auth_service_pb2.RegisterResponse()