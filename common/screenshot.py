import os
import allure
import time



def get_screenshot(driver, name):
    # 创建screenshots目录
    project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # screenshots_path = project_path + '\\screenshots\\'
    screenshots_path = os.path.join(project_path, 'screenshots')
    if not os.path.exists(screenshots_path):
        os.makedirs(screenshots_path)
    # 拼接截图的文件名（绝对路径）
    curr_time = time.strftime("%Y%m%d_%H%M%S")
    # filename = screenshots_path + name + "_" + curr_time + '.png'
    filename = os.path.join(screenshots_path, f'{name}_{curr_time}.png')
    driver.get_screenshot_as_file(filename)
    # 截图文件附加到allure报告中
    allure.attach.file(source=filename, name=f"{name}"+"_"+f"{curr_time}", attachment_type=allure.attachment_type.PNG)

