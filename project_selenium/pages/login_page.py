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

    #页面元素定位器
    USERNAME_INPUT = (By.CSS_SELECTOR,'input[placeholder="输入用户名"]')
    PASSWORD_INPUT = (By.CSS_SELECTOR,'input[placeholder="输入密码"]')
    LOGIN_BUTTON = (By.CLASS_NAME,"login-button")

    def login(self):
        """
        从配置文件中读取用户名，密码和URL，然后完成页面交互
        """
        try:
            #Get the username and password from config.ini
            #从配置文件中读取账户和地址
            username = ConfigManager.get_from_config("credentials","username")
            password = ConfigManager.get_from_config("credentials","password")
            base_url = ConfigManager.get_from_config("urls","base_url")

            # #####
            # print(username)
            # print(password)
            # print(base_url)
            # #####

            self.driver.get(base_url)
            #self.driver.implicitly_wait(3)
            self.logger.info(f"Navigated to {base_url}")

            #输入用户名，密码，点击登录
            self.input_text(self.USERNAME_INPUT,username,"Username Input")
            self.input_text(self.PASSWORD_INPUT,password,"Password Input")
            self.click(self.LOGIN_BUTTON,"Login Button")
            self.logger.info("Login successful")
            sleep(5)

        except Exception as e:
            self.logger.error(f"登录失败:{str(e)}")
            self._take_screenshot("login_failed")
            raise

    def login_with_credentials(self,username,password):
        """
        使用用户名和密码执行登录操作(用于数据驱动测试)
        """
        try:
            base_url = ConfigManager.get_from_config("urls", "base_url")

            self.driver.get(base_url)
            self.driver.implicitly_wait(3)
            self.logger.info(f"Navigated to {base_url}")

            self.input_text(self.USERNAME_INPUT, username, "Username Input")
            self.input_text(self.PASSWORD_INPUT, password, "Password Input")
            self.click(self.LOGIN_BUTTON, "Login Button")

            # 显式等待 登录按钮消失，最多等10秒
            WebDriverWait(self.driver, 10).until_not(
                EC.visibility_of_element_located(self.LOGIN_BUTTON)
            )

            self.logger.info(f"Login successful for user:{username}")
            #sleep(2)

        except Exception as e:
            self.logger.error(f"登录失败 - 用户：{username} 错误:{str(e)}")
            self._take_screenshot("login_failed")
            raise


    def is_welcome_shown(self,username):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//h4[contains(text(),'欢迎进入')]"))
            )
            element = self.driver.find_element(By.XPATH, "//h4[contains(text(),'欢迎进入')]")
            print("-------------")
            print(element)
            print("-------------")
            visible1 = element.is_displayed()

            if not visible1:
                self.driver.save_screenshot("login_fail.png")
                self.logger.error(f"登录失败 - 用户：{username},元素存在但不可见")
                print("登录失败,不可见'欢迎进入'字样")
            else:
                self.logger.info(f"登录成功 - 用户：{username}")
            return visible1
        except TimeoutException as e:
            # 等待超时，元素一直没显示出来，可能是不存在或者一直不可见
            self._take_screenshot("login_failed_welcome_timeout.png")
            self.logger.error(f"登录失败 - 用户：{username}，等待元素可见超时 错误：{str(e)}")
            print("登录后没有找到欢迎进入文案，等待超时")
            return False

        except NoSuchElementException as e:
            self._take_screenshot("login_failed_welcome.png")
            self.logger.error(f"登录失败 - 用户：{username}，页面没有找到元素 错误：{str(e)}")
            print("登录后没有找到欢迎进入文案，元素未找到")
            return False