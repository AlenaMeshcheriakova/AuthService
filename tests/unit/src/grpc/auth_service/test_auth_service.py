import threading
import grpc
import pytest

from src.grpc.auth_service import auth_service_pb2_grpc, auth_service_pb2
from tests.unit.src.grpc.auth_service.mock_auth_service import serve
from tests.unit.test_data_preparation import DataPreparation, create_test_user


@pytest.fixture(scope='module')
def grpc_channel():
    stop_event = threading.Event()
    server, wait_for_stop = serve(stop_event)

    yield grpc.insecure_channel('localhost:50051')

    stop_event.set()
    wait_for_stop()

@pytest.fixture
def grpc_stub(grpc_channel):
    return auth_service_pb2_grpc.AuthServiceStub(grpc_channel)

class TestAuthService:
    """Group of Unit-Tests for class AuthServiceServicer"""

    def test_login_success(self, grpc_stub):
        request = auth_service_pb2.LoginRequest(username=DataPreparation.TEST_USER_NAME, password=DataPreparation.TEST_PASS)

        response = grpc_stub.login(request)

        assert response.token == "mock_access_token"
        assert response.expires_in == "15"

    def test_login_failure(self, grpc_stub):
        request = auth_service_pb2.LoginRequest(username=DataPreparation.TEST_USER_NAME, password="wrong_password")

        with pytest.raises(grpc.RpcError) as excinfo:
            grpc_stub.login(request)

        assert excinfo.value.code() == grpc.StatusCode.UNAUTHENTICATED
        assert excinfo.value.details() == "Invalid credentials"

    def test_validate_token_success(self, grpc_stub):
        request = auth_service_pb2.ValidateTokenRequest(token="valid_token")

        response = grpc_stub.validate_token(request)

        assert response.is_valid is True
        assert response.user_id == str(DataPreparation.TEST_USER_ID)
        assert response.email == DataPreparation.TEST_USER_EMAIL
        assert response.username == DataPreparation.TEST_USER_NAME

    def test_validate_token_failure(self, grpc_stub):
        request = auth_service_pb2.ValidateTokenRequest(token="invalid_token")

        response = grpc_stub.validate_token(request)

        assert response.is_valid is False

    def test_register_success(self, grpc_stub):
        request = auth_service_pb2.RegisterRequest(
            username=DataPreparation.TEST_USER_NAME,
            email=DataPreparation.TEST_USER_EMAIL,
            password=DataPreparation.TEST_PASS,
            telegram_user_id=DataPreparation.TEST_TELEGRAM_USER_ID
        )

        response = grpc_stub.register(request)

        assert response.username == DataPreparation.TEST_USER_NAME
        assert response.message == "User registered successfully"

    def test_register_failure(self, grpc_stub, create_test_user):
        request = auth_service_pb2.RegisterRequest(
            username="existing_user",
            email=DataPreparation.TEST_USER_EMAIL,
            password=DataPreparation.TEST_PASS,
            telegram_user_id=DataPreparation.TEST_TELEGRAM_USER_ID
        )

        with pytest.raises(grpc.RpcError) as excinfo:
            grpc_stub.register(request)

        assert excinfo.value.code() == grpc.StatusCode.ALREADY_EXISTS
        assert excinfo.value.details() == "User already exists"