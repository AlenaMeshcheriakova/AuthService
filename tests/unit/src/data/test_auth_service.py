import datetime

from src.data.auth_service import AuthOrm
from src.db.database import session_factory
from src.model.userdb import UserDB
from tests.unit.test_data_preparation import (DataPreparation, create_test_user)

class TestAuthOrm:
    """Group of Unit-Tests for class AuthOrm"""

    def test_get_user_by_email(self, create_test_user):
        """
        Test for a method - get user by email
        """
        user = AuthOrm.get_user_by_email(DataPreparation.TEST_USER_EMAIL)
        assert user is not None
        assert user.email == DataPreparation.TEST_USER_EMAIL

    def test_get_user_by_username(self, create_test_user):
        """
        Test for a method - get a user by username
        """
        user = AuthOrm.get_user_by_username(DataPreparation.TEST_USER_NAME)
        assert user is not None
        assert user.user_name == DataPreparation.TEST_USER_NAME

    def test_create_user(self):
        """
        Test for creating a new user
        """
        email = DataPreparation.TEST_USER_EMAIL
        password = DataPreparation.TEST_PASS
        username = DataPreparation.TEST_USER_NAME
        telegram_user_id = DataPreparation.TEST_TELEGRAM_USER_ID

        new_user = AuthOrm.create_user(email, password, username, telegram_user_id)

        assert new_user is not None
        assert new_user.email == email
        assert new_user.user_name == username

        # Verify in the database
        with session_factory() as session:
            db_user = session.query(UserDB).filter_by(email=email).first()
            assert db_user is not None
            assert db_user.email == email
            assert db_user.user_name == username

    def test_create_access_token(self):
        """
        Test for creating an access token
        """
        data = {"sub": "test_user"}
        expires_delta = datetime.timedelta(minutes=15)
        token = AuthOrm.create_access_token(data, expires_delta)

        assert token is not None
        assert isinstance(token, str)

    def test_verify_token(self):
        """
        Test for verifying a token
        """
        data = {"sub": "test_user"}
        expires_delta = datetime.timedelta(minutes=15)
        token = AuthOrm.create_access_token(data, expires_delta)

        token_data = AuthOrm.verify_token(token)
        assert token_data is not None
        assert token_data.username == "test_user"