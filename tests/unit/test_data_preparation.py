import uuid
import pytest
from src.db.database import session_factory
from src.model.userdb import UserDB

class DataPreparation:
    # User
    TEST_USER_ID = uuid.uuid4()
    TEST_USER_AUTH_ID = uuid.uuid4()
    TEST_USER_NAME = 'TEST_USER_NAME'
    TEST_USER_EMAIL = 'TEST_USER_EMAIL@gmail.com'
    TEST_PASS = 'TEST_PASS'
    TEST_TELEGRAM_USER_ID = "12341234"

@pytest.fixture(scope="function")
def create_test_user():
    """
    Fixture to create a test AUTH user in the database.
    """
    with session_factory() as session:
        test_user = UserDB(
            id=DataPreparation.TEST_USER_ID,
            email=DataPreparation.TEST_USER_EMAIL,
            password=DataPreparation.TEST_PASS,
            user_name=DataPreparation.TEST_USER_NAME,
            telegram_user_id=DataPreparation.TEST_TELEGRAM_USER_ID
        )
        session.add(test_user)
        session.commit()
        yield test_user