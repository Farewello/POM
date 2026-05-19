from pages.base_page import BasePage
from pages.home_page import HomePage
from common.read_config import project_root_path
import os

class LoginPage(BasePage):

    # yaml_path = r'D:\POM\page_yaml\LoginPage.yaml'  #todo:后续修改路径
    yaml_path = os.path.join(project_root_path, 'page_yaml', 'LoginPage.yaml')


    #使用账号密码登录
    def use_account_pwd_login(self, mobile, pwd):
        self.run_steps(LoginPage.yaml_path, 'use_account_pwd_login', mobile=mobile, pwd=pwd)
        home_page = HomePage(self.driver)
        return home_page



if __name__ == '__main__':
    HomePage().goto_login_page().use_account_pwd_login('13311122233', '123456zz')