import os
import yaml

class ReadConfig:
    def __init__(self):
        #获取当前绝对地址
        self.root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        #拼接配置文件的绝对地址
        self.config_path = os.path.join(self.root_path, 'config', 'config.yaml')

    #读取config
    def get_config(self):
        with open(self.config_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        return data

#实例化
config_data = ReadConfig().get_config()
project_root_path = ReadConfig().root_path

