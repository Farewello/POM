from pages.base_page import BasePage
from common.read_config import project_root_path
import os
from common.read_config import config_data


class HomePage(BasePage):
    # yaml_path = r'D:\POM\page_yaml\HomePage.yaml'  #todo:后续更改为相对路径
    yaml_path = os.path.join(project_root_path, 'page_yaml', 'HomePage.yaml')
    #进入登录页面
    def goto_login_page(self):
        self.run_steps(HomePage.yaml_path, 'goto_login_page')
        from pages.login_page import LoginPage
        return LoginPage(self.driver)

    #获取登录名
    def get_login_name(self):
        element = self.run_steps(HomePage.yaml_path, 'get_login_name')
        login_name_text = element.text.strip()
        return login_name_text
        # assert login_name == '12'

    #移动到登录名
    def move_to_login_name(self):
        self.run_steps(HomePage.yaml_path, 'move_to_login_name')
        return self

    #退出登录
    def login_out(self):
        self.run_steps(HomePage.yaml_path, 'login_out')
        return self

    #验证退出登录成功（显示登录按钮）
    def login_btn_is_displayed(self):
        login_btn = self.run_steps(HomePage.yaml_path, 'login_btn_is_displayed')
        return login_btn.is_displayed()

    #搜索商品
    def search_goods(self, good_name):
        elements = self.run_steps(HomePage.yaml_path, 'search_goods', good_name=good_name)
        return elements

    #进入商品详情
    def goto_good_detail(self, good_name, index:int):
        elements = self.search_goods(good_name)
        if not elements:
            raise AssertionError(f"搜索 '{good_name}' 未返回任何商品")
        if index < 1 or index > len(elements):
            raise IndexError(f"商品数量 {len(elements)}，无法选择第 {index} 个")
        element = elements[index - 1]
        self.run_steps(HomePage.yaml_path, 'goto_good_detail', index=index)
        return self

if __name__ == '__main__':
    HomePage().goto_login_page().use_account_pwd_login(config_data['base']['mobile'], config_data['base']['pwd']).goto_good_detail(config_data['base']['good_name'], 1)


