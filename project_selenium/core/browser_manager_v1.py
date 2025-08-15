#browser_manager.py

import logging
import tempfile
import uuid
import shutil
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from utils.config_manager import ConfigManager

class BrowserManager:
    """
    浏览器管理类：统一负责启动和关闭Selenium浏览器。
    """

    def __init__(self):
        """
        初始化，读取配置文件，准备浏览器选项。
        """
        self.driver = None
        self.wait = None
        self.logger = logging.getLogger(__name__)

        #配置文件中是headless = False，需要转换
        self.headless_mode = ConfigManager.get_from_config("browser", "headless")

        #创建浏览器配置对象
        self.options = Options()

        #方案一
        #为每个浏览器实例使用唯一的user-data-dir,避免并发冲突
        #创建的目录在C:\Users\myname\AppData\Local\Temp\
        self.user_data_dir = os.path.join(
            tempfile.gettempdir(),f"chrome_user_{uuid.uuid4().hex}"
        )
        os.makedirs(self.user_data_dir,exist_ok=True)
        print("=======================")
        print("使用的用户数据目录",self.user_data_dir)
        print("=======================")
        self.options.add_argument(f"--user-data-dir={self.user_data_dir}")

        # #方案二
        # #无痕模式
        # self.options.add_argument("--incognito")

        # #方案三
        # #访客模式
        # self.options.add_argument("--guest")


        # 设置浏览器的基本启动参数
        self._setup_options()

    def _setup_options(self):
        """配置浏览器选项"""

        #启动时最大化窗口
        self.options.add_argument("--start-maximized")

        ## UI 相关（更干净）
        #禁用浏览器拓展插件，防止某些插件干扰脚本（如广告拦截器、插件等）
        self.options.add_argument("--disable-extensions")

        ## 反检测（更像人工）
        #与JS注入重复
        # #去除navigator.webdriver=true，防止被检测为机器人
        # self.options.add_argument("--disable-blink-features=AutomationControlled")

        #去掉浏览器顶部“自动化控制”的提示
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        #禁用Selenium加载的默认自动化拓展
        self.options.add_experimental_option('useAutomationExtension', False)

        # 暂时不启用headless模式。
        # # 启用无头模式（如果配置中设置为 true）
        # if self.headless_mode:
        #     self.options.add_argument("--headless=new")
        #     self.options.add_argument("--disable-gpu")  # 避免某些图形渲染 bug
        #     self.options.add_argument("--window-size=1920,1080")  # 设置默认分辨率，确保截图完整


    def start_browser(self,browser_type="chrome"):
        """
        启动浏览器
        """
        try:
            print(f"正在启动浏览器")
            self.logger.info("正在启动Chrom浏览器(自我驱动管理)...")
            #print(f"无头模式状态: {self.headless_mode}")

            #启动Chrome浏览器服务
            service = ChromeService(executable_path=ChromeDriverManager().install())
            #创建 webDriver 实例
            driver = webdriver.Chrome(service=service, options=self.options)

            #注入 JS 脚本，将 navigator.webdriver 设置为 undefined
            driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": """
                           Object.defineProperty(navigator, 'webdriver', {get: () => undefined})
                       """
            })

            print("Chrome启动成功！")

            #把局部driver 赋值给self.driver
            self.driver = driver
            #智能等待，元素是否出现在页面上并且是可见的，最多等待10S。
            self.wait = WebDriverWait(self.driver, 10)

            return self.driver

        except Exception as e:
            self.logger.error(f"浏览器启动失败:{e}",exc_info=True)
            self._force_kill_chrome()
            self._cleanup_user_data_dir()
            raise RuntimeError(f"浏览器启动失败: {str(e)}")


    def close_browser(self, driver):
        """关闭浏览器并清理目录"""
        try:
            if driver:
                driver.quit()
        except Exception as e:
            self.logger.warning(f"关闭浏览器时报错:{e}")
        finally:
            self._cleanup_user_data_dir()

    def _cleanup_user_data_dir(self):
        """删除临时的用户数据目录"""
        if getattr(self, "user_data_dir", None):
            try:
                shutil.rmtree(self.user_data_dir, ignore_errors=True)
                self.logger.info(f"已删除临时用户数据目录: {self.user_data_dir}")
            except Exception as e:
                self.logger.warning(f"删除临时目录失败: {e}")

    def _force_kill_chrome(self):
        """强制杀掉残留 Chrome 进程，避免 user-data-dir 锁冲突"""
        try:
            if platform.system() == "Windows":
                subprocess.run("taskkill /F /IM chrome.exe /T", shell=True,
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                subprocess.run("pkill -f chrome", shell=True,
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception as e:
            self.logger.warning(f"强制结束 Chrome 进程失败: {e}")