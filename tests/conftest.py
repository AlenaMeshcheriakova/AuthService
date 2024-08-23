import logging
import pytest

from src.db.base import Base
from cfg.сonfig import settings
from src.db.database import sync_engine, session_factory

@pytest.fixture(autouse=True, scope='session')
def prepare_database():
    """
    Create all tables at the beginning of all tests and Drop all tables when is finished
    """
    logging.info("Start creating tables... ")
    assert settings.MODE == "TEST"
    Base.metadata.create_all(sync_engine)
    yield
    logging.info("Start deleting tables... ")
    assert settings.MODE == "TEST"
    Base.metadata.drop_all(sync_engine)

@pytest.fixture(autouse=True, scope="function")
def cleanup(request):
    """Cleanup method - started up in the after each function
    :param request: parameters from the startup
    """
    def remove_test_dir():
        logging.info("Start cleaning data... ")
        assert settings.MODE == "TEST"
        with session_factory() as session:
            for table in reversed(Base.metadata.sorted_tables):
                session.execute(table.delete())
            session.commit()
    request.addfinalizer(remove_test_dir)
