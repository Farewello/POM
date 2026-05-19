from pages.home_page import HomePage
from common.log import MyLogger
from common.screenshot import get_screenshot
import pytest

logger = MyLogger().get_logger()

class TestLogin:
    @pytest.mark.parametrize('mobile, pwd, username',[
        ('13311122233', '123456zz', '12'),
        ('17712312377', '123456.', '德云测自动化')
    ])
    def test_login(self,base_driver, mobile, pwd, username):
        try:
            logger.info('用例执行：test_login')
            login_name_text = HomePage(base_driver).goto_login_page().use_account_pwd_login(mobile, pwd).get_login_name()
            assert login_name_text == username
        except Exception as e:
            logger.error(e)
            logger.info('用例执行失败')
            get_screenshot(base_driver, 'test_login')
            raise e
        else:
            logger.info('用例：test_login执行通过')


