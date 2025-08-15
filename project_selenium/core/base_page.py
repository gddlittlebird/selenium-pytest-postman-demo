#base_page.py

import os
import logging
from  datetime import datetime
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.config_manager import ConfigManager


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
        #设置隐式等待(全局)，在定位元素时最多等待 2 秒
        driver.implicitly_wait(2)

        #设置显示等待(用于显示等待)
        self.wait = WebDriverWait(driver,10)

        #日志记录器
        self.logger = logging.getLogger(__name__)

        #截图保留目录
        self.screenshots_dir = ConfigManager.get_screenshots_dir()


    def _take_screenshot(self,name):
        """
        截取当前屏幕并保存到 screenshot 文件夹。
        :param name: 文件前缀
        """

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.screenshots_dir,f"{name}_{timestamp}.png")
        self.driver.save_screenshot(filename)
        self.logger.info(f"Screenshot saved:{filename}")


    def click(self,locator,element_name=""):
        """
        点击元素(显示等待直到可点击)
        :param locator: 元素定位元组，例如(By.ID,"submit")
        :param element_name: 元素名称(用于日志记录，可选)
        """
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
            self.logger.info(f"Click element：{element_name or locator}")
        except Exception as e:
            self.logger.error(f"Click Failed：{element_name or locator} - Error:{str(e)}")
            self._take_screenshot("click_error")
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
            self.logger.info(f"Input '{text}' to:{element_name or locator}")
        except Exception as e:
            self.logger.error(f"Input failed {element_name or locator} - Error:{str(e)}")
            self._take_screenshot("input_error")
            raise


    def get_text(self,locator,element_name=""):
        """
        获取元素文本内容
        """
        try:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            text = element.text
            self.logger.info(f"Retrieved text from {element_name or locator}:'{text}'")
            return text
        except Exception as e:
            self.logger.error(f"Get Text Failed {element_name or locator} - Error {str(e)}")
            self._take_screenshot("get_text_error")
            raise


    def is_visible(self,locator,element_name=""):
        """
        判断元素是否在页面中可见，返回布尔值
        """

        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            self.logger.info(f"Element is visible: {element_name or locator}")
            return True
        except Exception as e:
            self.logger.warning(f"Element not visible:{element_name or locator} - Error:{str(e)}")
            return False

    def scroll_into_view(self,locator,element_name=""):
        """
        将元素滚动可视页面中，使其可操作。
        """
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            self.driver.execute_script("arguments[0].scrollIntoView(true)",element)
            self.logger.info(f"Scrolled into view: {element_name or locator}")
        except Exception as e:
            self.logger.error(f"[Scroll Failed] {element_name or locator} - Error: {str(e)}")
            self._take_screenshot("scroll_error")
            raise













