import pytest
from common.read_config import config_data

from pages.home_page import HomePage


@pytest.fixture(scope="session")
def base_driver():
    homepage = HomePage()
    driver = homepage.driver
    yield driver
    driver.quit()

@pytest.fixture(scope="function", autouse=True)
def reset_state(base_driver):
    base_driver.delete_all_cookies()
    base_driver.get(config_data['base']['url'])