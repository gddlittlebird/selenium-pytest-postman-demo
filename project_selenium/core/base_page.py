#base_page.py

import os
import logging
from  datetime import datetime

from selenium.common import ElementClickInterceptedException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotSelectableException
from utils.config_manager import ConfigManager
from utils.logger import get_logger
import time


class BasePage:
    """
    所有页面对象的基类，封装了基础操作：
    -显示等待
    -点击
    -输入文本
    -获取文本
    -判断是否可见
    -滚动视图
    -错误时截图 + 日志
    """

    def __init__(self,driver):
        """
        初始化页面对象。
        :param driver: webDriver实例
        """

        self.driver = driver

        #每个页面对象都有一个日志记录器，文件名自动按类名生成
        self.logger = get_logger(self.__class__.__name__)

        #设置隐式等待(全局)，在定位元素时最多等待 2 秒
        driver.implicitly_wait(2)

        #设置显示等待(用于显示等待)
        self.wait = WebDriverWait(driver,10)

        #截图保留目录
        self.screenshots_dir = ConfigManager.get_screenshots_dir()

    def _take_screenshot(self,name):
        """
        截取当前屏幕并保存到 screenshot 文件夹。
        :param name: 文件前缀
        """
        filename = os.path.join(self.screenshots_dir,f"{name}.png")
        self.driver.save_screenshot(filename)
        self.logger.info(f"Screenshot saved:{filename}")

    def _format_element(self,locator,element_name=""):
        name = element_name if element_name else "未命名元素"
        return f"{name}[{locator[0]}={locator[1]}]"

    def handle_error(self,step_name:str,exception:Exception):
        """
        统一的错误处理方法：记录日志 + 截图
        :param step_name: 当前步骤名称(比如‘预报下单')
        :param exception:捕获到的异常
        :return:
        """
        self.logger.error(f"{step_name}, 错误类型: {type(exception).__name__}, 错误信息:{exception}")
        self._take_screenshot(f"{step_name}_failed_{self._timestamp()}")

    def click(self,locator,element_name=""):
        """
        点击元素(自动处理滚动和遮挡)
        :param locator: 元素定位元组，例如(By.ID,"submit")
        :param element_name: 元素名称(用于日志记录，可选)
        """
        try:
            # 1.尝试直接点击
            element = self.wait.until(EC.element_to_be_clickable(locator))
            try:
                element.click()
                self.logger.info(f"Click element：{self._format_element(locator,element_name)}")
            except ElementClickInterceptedException:
                # 2.如果被遮挡或不可见，尝试到视野再用 JS 点击
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                self.driver.execute_script("arguments[0].click();", element)
                self.logger.info(f"Click element(JS):{self._format_element(locator,element_name)}")
        except Exception as e:
            self.handle_error(f"Click Failed: {self._format_element(locator, element_name)}", e)
            raise


    def input_text(self,locator,text,element_name=""):
        """
        清空并向输入框中输入文本。
        :param locator: 元素定位元组
        :param text: 输入的内容
        :param element_name: 元素名称(用于日志记录，可选)
        :return:
        """
        try:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            element.clear()
            element.send_keys(text)
            self.logger.info(f"Input '{text}' to:{self._format_element(locator,element_name)}")
        except Exception as e:
            self.handle_error(f"Input Failed：{self._format_element(locator,element_name)}",e)
            raise


    def get_text(self,locator,element_name=""):

        #获取元素文本内容
        try:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            text = element.text
            self.logger.info(f"Retrieved text from {self._format_element(locator,element_name)}:'{text}'")
            return text
        except Exception as e:
            self.handle_error(f"Get Text Failed：{self._format_element(locator,element_name)}",e)
            raise


    def is_visible(self,locator,element_name=""):
        """
        判断元素是否在页面中可见，返回布尔值
        """
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            self.logger.info(f"Element is visible: {self._format_element(locator,element_name)}")
            return True
        except Exception as e:
            self.handle_error(f"Is Visible Failed：{self._format_element(locator,element_name)}",e)
            return False


    def scroll_into_view(self,locator,element_name=""):
        """
        将元素滚动可视页面中，使其可操作。
        """
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            self.driver.execute_script("arguments[0].scrollIntoView(true)",element)
            self.logger.info(f"Scrolled into view: {self._format_element(locator,element_name)}")
        except Exception as e:
            self.handle_error(f"Scroll Failed：{self._format_element(locator,element_name)}",e)
            raise

    def select_from_dropdown(self, input_locator, option_locator_func, value, element_name="Dropdown"):
        """
        简单风格的通用下拉选择方法（Vue/Element UI 下拉框）

        步骤：
        1. 等待输入框可点击
        2. 滚动到输入框
        3. 等待下拉选项可见
        4. JS 点击选项
        5. 日志记录

        :param input_locator: 输入框定位，例如 (By.XPATH, "//input[@placeholder='请输入']")
        :param option_locator_func: 函数，根据 value 生成下拉选项的定位
                                        例如 lambda v: (By.XPATH, f"//span[text()='{v}']")
        :param value: 要选择的值，例如 "客户A"
        :param element_name: 日志中显示的元素名称，默认 "Dropdown"
        """
        try:
            # 1. 等待输入框可点击
            input_element = self.wait.until(EC.element_to_be_clickable(input_locator))

            # 2. 滚动到输入框可见
            self.scroll_into_view(input_locator, element_name)
            # 3. 输入文字
            input_element.send_keys(value)
            self.logger.info(f"输入 {element_name}: {value}")
            # 4. 延迟 0.3 秒，等待下拉选项出现
            time.sleep(0.3)

            # 5. 等待下拉选项出现
            option_locator = option_locator_func(value)
            target_option = self.wait.until(EC.element_to_be_clickable(option_locator))

            # 6. 用 JS 点击选项
            self.driver.execute_script("arguments[0].click();", target_option)
            self.logger.info(f"选择 {element_name}: {value}")

        except Exception as e:
            self.handle_error(f"选择 {element_name} ", e)
            raise











