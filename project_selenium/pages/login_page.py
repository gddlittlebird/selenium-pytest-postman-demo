#login_page.py

from time import sleep

from selenium.common import TimeoutException

from core.base_page import BasePage
from selenium.webdriver.common.by import By
from utils.config_manager import ConfigManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

class LoginPage(BasePage):

    def __init__(self,driver):
        super().__init__(driver)

    #页面元素定位器
    USERNAME_INPUT = (By.CSS_SELECTOR,'input[placeholder="输入用户名"]')
    PASSWORD_INPUT = (By.CSS_SELECTOR,'input[placeholder="输入密码"]')
    LOGIN_BUTTON = (By.CLASS_NAME,"login-button")
    WELCOME_MESSAGE = (By.XPATH, "//h4[contains(text(),'欢迎进入')]")

    def _perform_login(self,username,password):
        """
        执行通用的登录流程
        """
        try:
            base_url = ConfigManager.get_from_config("urls","base_url")
            if not base_url:
                raise ValueError("Base URL not found in config.ini")
            self.driver.get(base_url)
            self.logger.info(f"Navigated to {base_url}")

            self.input_text(self.USERNAME_INPUT,username,"Username Input")
            self.input_text(self.PASSWORD_INPUT,password,"Password Input")
            self.click(self.LOGIN_BUTTON,"Login Button")

            # 显式等待 登录按钮消失，最多等10秒
            WebDriverWait(self.driver, 10).until_not(EC.visibility_of_element_located(self.LOGIN_BUTTON))
            self.logger.info(f"Login successful:{username}")

        except TimeoutException as e:
            self.handle_error("登录失败",e)
            raise


    def login(self):
        username = ConfigManager.get_from_config("credentials","username")
        password = ConfigManager.get_from_config("credentials","password")

        if not username or not password:
            raise ValueError("Username or password not found in config.ini")

        self._perform_login(username,password)

    def login_with_credentials(self,username,password):
        """
        使用用户名和密码执行登录操作(用于数据驱动测试)
        """
        self._perform_login(username,password)


    def is_welcome_shown(self,username):
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.WELCOME_MESSAGE)
            )

            if element.is_displayed():
                self.logger.info(f"登录成功 - 用户：{username}")
                return True
            else:
                self.logger.error(f"登录失败 - 用户：{username},元素存在但不可见")
                self._take_screenshot("login_failed_welcome_not_displayed.png")
                print("登录失败,不可见'欢迎进入'字样")
                return False
        except Exception as e:
            self.handle_error("没有‘欢迎字样’",e)
            raise
