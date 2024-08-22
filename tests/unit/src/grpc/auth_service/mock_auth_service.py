import grpc
from concurrent import futures
import pytest
from unittest.mock import patch
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta
from src.grpc.auth_service import auth_service_pb2_grpc, auth_service_pb2
from tests.unit.test_data_preparation import DataPreparation


class MockAuthServiceServicer(auth_service_pb2_grpc.AuthServiceServicer):
    """
    Mock behavior for methods in AuthServiceServicer
    """

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def login(self, request, context):
        if request.username == DataPreparation.TEST_USER_NAME and request.password == DataPreparation.TEST_PASS:
            access_token = "mock_access_token"
            return auth_service_pb2.LoginResponse(token=access_token, expires_in="15")
        else:
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details("Invalid credentials")
            return auth_service_pb2.LoginResponse()

    def validate_token(self, request, context):
        try:
            if request.token == "valid_token":
                return auth_service_pb2.ValidateTokenResponse(
                    is_valid=True,
                    user_id=str(DataPreparation.TEST_USER_ID),
                    email=DataPreparation.TEST_USER_EMAIL,
                    username=DataPreparation.TEST_USER_NAME
                )
            else:
                return auth_service_pb2.ValidateTokenResponse(is_valid=False)
        except Exception as e:
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details(str(e))
            return auth_service_pb2.ValidateTokenResponse(is_valid=False)

    def register(self, request, context):
        if request.username == "existing_user":
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            context.set_details("User already exists")
            return auth_service_pb2.RegisterResponse()
        else:
            return auth_service_pb2.RegisterResponse(username=request.username, message="User registered successfully")

def serve(stop_event):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    auth_service_pb2_grpc.add_AuthServiceServicer_to_server(MockAuthServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()

    def wait_for_stop():
        stop_event.wait()
        server.stop(grace=None)
    return server, wait_for_stop