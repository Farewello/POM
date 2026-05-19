from pages.home_page import HomePage
from common.log import MyLogger
from common.screenshot import get_screenshot
from common.read_config import config_data

logger =  MyLogger().get_logger()
class TestSearchGood:
    def test_search_good(self, base_driver):
        logger.info('用例执行：test_search_good')
        try:
            elements = HomePage(base_driver).goto_login_page().use_account_pwd_login(config_data['base']['mobile'], config_data['base']['pwd']).search_goods(config_data['base']['good_name'])
            # assert config_data['base']['good_name'] in goods_list
            goods_list = [element.text.strip() for element in elements]
            # 检查获取到的商品列表中，是否至少有一个商品的名称包含了 "自动化"
            assert any(config_data['base']['good_name'] in good for good in
                       goods_list), f"搜索结果不匹配，实际结果为: {goods_list}"

        except Exception as e:
            logger.error(e)
            logger.info('用例执行失败：test_search_good')
            get_screenshot(base_driver,'test_search_good')
            raise e
        else:
            logger.info('用例执行成功：test_search_good')