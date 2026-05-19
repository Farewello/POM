import os
import time
from string import Template
import yaml
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from common.read_config import config_data, project_root_path

class BasePage:
    #打开浏览器
    def __init__(self, driver=None):
        self.config = config_data
        timeout = self.config['base']['timeout']
        if driver is None:
            driver_sub_path = self.config['base']['driver_path']
            driver_path = str(os.path.join(project_root_path, driver_sub_path))
            base_url = self.config['base']['url']

            # driver_path = r'D:\POM\common\driver\chromedriver.exe'  #todo:后续更改相对路径
            service = Service(executable_path=driver_path)
            self.driver = webdriver.Chrome(service=service)
            #隐式等待
            self.driver.implicitly_wait(timeout)
            #显示等待
            self.wait = WebDriverWait(self.driver, timeout)
            #浏览器最大化
            self.driver.maximize_window()
            self.driver.get(base_url)
        else:
            self.driver = driver
            self.wait = WebDriverWait(self.driver, timeout)

    #关闭浏览器
    def quit_browser(self):
        self.driver.quit()

    #简化定位器表达式
    @staticmethod
    def get_by_locator(by, locator):
        if by == 'id':
            by_locator = (By.ID, locator)
        elif by == 'name':
            by_locator = (By.NAME, locator)
        elif by == 'class':
            by_locator = (By.CLASS_NAME, locator)
        elif by == 'tag':
            by_locator = (By.TAG_NAME, locator)
        elif by == 'link':
            by_locator = (By.LINK_TEXT, locator)
        elif by == 'part':
            by_locator = (By.PARTIAL_LINK_TEXT, locator)
        elif by == 'xpath':
            by_locator = (By.XPATH, locator)
        elif by == 'css':
            by_locator = (By.CSS_SELECTOR, locator)
        else:
            raise ValueError(f'定位方式by没有根据传入，请联系相关负责人员，当前错误方式：{by}')
        return by_locator
    #定位单元素
    def find(self, by, locator):
        by_locator = self.get_by_locator(by, locator)
        #正常
        # element = self.driver.find_element(by_locator)
        #加入显示等待
        element = self.wait.until(ec.visibility_of_element_located(by_locator))
        return element

    #定位单元素并点击
    def find_and_click(self, by, locator):
        element = self.find(by, locator)
        element.click()

    #定位单元素并输入
    def find_and_send(self, by, locator, text):
        element = self.find(by, locator)
        element.clear()
        element.send_keys(text)

    #定位多个元素
    def finds(self, by, locator):
        by_locator = self.get_by_locator(by, locator)
        elements = self.wait.until(ec.visibility_of_all_elements_located(by_locator))
        return elements

    #定位多个元素，返回指定单元素
    def find_by_index(self, by, locator, index):
        elements = self.finds(by, locator)
        if index < 0 or index > len(elements):
            raise IndexError(f'当前索引错误,当前元素个数：{len(elements)}, 传入索引：{index}')
        return elements[index - 1]

    #多元素种单元素点击
    def finds_and_click(self, by, locator, index):
        element = self.find_by_index(by, locator, index)
        element.click()


    #多元素中单元素输入
    def finds_and_send(self, by, locator, index, text):
        element = self.find_by_index(by, locator, index)
        element.clear()
        element.send_keys(text)

    #移动鼠标
    def move_to_element(self, by, locator, index=None):
        if index is None:
          element = self.find(by, locator)
        else:
            elements = self.finds(by, locator)
            element = elements[index]
        ActionChains(self.driver).move_to_element(element).perform()

    #字符串替换

    @staticmethod
    def _render_value(value, kwargs):
        if isinstance(value, str):
            # 1. 完整变量匹配：如果 YAML 里的值刚好是 "$变量名"
            if value.startswith('$') and value[1:] in kwargs:
                # 直接返回 kwargs 里的原始对象（如果是整数，返回的就是整数；如果是列表，就是列表）
                return kwargs[value[1:]]

            # 2. 字符串拼接匹配：如果是类似 "前缀_$text_后缀" 的混合字符串
            if '$' in value:
                return Template(value).safe_substitute(kwargs)

        # 3. 其他情况（如 None，或者本来就是数字）直接返回原值
        return value
    #读取操作方法
    def run_steps(self, yaml_file, function_name, **kwargs):
        with open(yaml_file, 'r', encoding='utf-8') as f:
            yaml_data = yaml.safe_load(f)

            steps = yaml_data[function_name]
            for step in steps:
                action = step['action']
                locator = step.get('locator')
                # index = step.get('index')
                index = self._render_value(step.get('index'), kwargs)

                # raw_index = self._render_value(step.get('index'), kwargs)
                # index = int(raw_index) if isinstance(raw_index, str) and raw_index.isdigit() else raw_index
                text = self._render_value(step.get('text'), kwargs)
                sleep = step.get('sleep')

                result = None
                if action == 'find':
                    result = self.find(*locator)
                elif action == 'find_and_click':
                    self.find_and_click(*locator)
                elif action == 'find_and_send':
                    self.find_and_send(*locator, text)
                elif action == 'finds':
                    result = self.finds(*locator)
                elif action == 'finds_and_click':
                    self.finds_and_click(*locator, index)
                elif action == 'finds_and_send':
                    self.finds_and_send(*locator, index, text)
                elif action == 'move_to_element':
                    self.move_to_element(*locator, index)
                else:
                    raise ValueError(f'读取到错误关键字：{action}')

                if sleep:
                    time.sleep(sleep)
            return result



if __name__ == "__main__":
    BasePage()
