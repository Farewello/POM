from pages.home_page import HomePage
from common.log import MyLogger
from common.screenshot import get_screenshot
from common.read_config import config_data


logger = MyLogger().get_logger()

class TestLoginOut:
    def test_login_out(self, base_driver):
        logger.info('执行用例：test_login_out(使用正确账号密码登录)')
        try:
            result = HomePage(base_driver).goto_login_page().use_account_pwd_login( config_data['account']['mobile'], config_data['account']['pwd']).move_to_login_name().login_out().login_btn_is_displayed()
            assert result is True
        except Exception as e:
            logger.error(e)
            logger.info('执行用例：test_login_out(使用正确账号密码登录)失败')
            get_screenshot(base_driver, 'test_login_out')
            raise e
        else:
            logger.info('用例执行通过')

