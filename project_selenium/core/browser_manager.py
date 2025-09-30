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
    支持两种模式:
    - 顺序执行模式（固定用户数据目录，模拟人工操作）
    - 并发执行模式（每个实例一个临时用户数据目录）
    """

    def __init__(self,parallel=False):
        """
        :param parallel: True 表示并发执行（每个浏览器实例独立临时目录）
        """
        self.driver = None
        self.wait = None
        self.logger = logging.getLogger(__name__)
        self.parallel = parallel
        self.user_data_dir = None

        #配置文件中是headless = False，需要转换
        raw_headless = ConfigManager.get_from_config("browser", "headless") or False
        self.headless_mode = False if raw_headless == "False" else True


    def _create_user_data_dir(self):
        """根据模式创建用户数据目录"""
        try:
            if self.parallel:
                # 每个实例用唯一目录
                self.user_data_dir = tempfile.mkdtemp(prefix=f"chrome_profile_{uuid.uuid4().hex}_")
            else:
                # 固定目录，模拟人工
                self.user_data_dir = os.path.expanduser(os.path.join("~", ".selenium_chrome_profile"))
                os.makedirs(self.user_data_dir, exist_ok=True)
        except Exception as e:
            self.logger.error(f"创建用户数据目录失败: {e}",exc_info=True)
            raise RuntimeError(f"创建用户数据目录失败: {str(e)}")

    def _setup_options(self):
        """配置浏览器选项"""
        options = Options()
        options.add_argument(f"--user-data-dir={self.user_data_dir}")

        #启动时最大化窗口
        options.add_argument("--start-maximized")

        ## UI 相关（更干净）
        #禁用浏览器拓展插件，防止某些插件干扰脚本（如广告拦截器、插件等）
        options.add_argument("--disable-extensions")

        ## 反检测（更像人工）
        #与JS注入重复
        # #去除navigator.webdriver=true，防止被检测为机器人
        # self.options.add_argument("--disable-blink-features=AutomationControlled")

        #去掉浏览器顶部“自动化控制”的提示
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        #禁用Selenium加载的默认自动化拓展
        options.add_experimental_option('useAutomationExtension', False)

        # 暂时不启用headless模式。
        # # 启用无头模式（如果配置中设置为 true）
        # if self.headless_mode:
        #     self.options.add_argument("--headless=new")
        #     self.options.add_argument("--disable-gpu")  # 避免某些图形渲染 bug
        #     self.options.add_argument("--window-size=1920,1080")  # 设置默认分辨率，确保截图完整

        return options


    def start_browser(self,browser_type="chrome"):
        """启动浏览器"""
        try:
            self._create_user_data_dir()
            options = self._setup_options()

            self.logger.info(f"启动Chrome(自我驱动管理),用户数据目录:{self.user_data_dir}")
            print(f"启动Chrome,用户数据目录:{self.user_data_dir}")
            # print(f"无头模式状态: {self.headless_mode}")

            # 启动Chrome浏览器服务
            service = ChromeService(executable_path=ChromeDriverManager().install())
            # 创建 webDriver 实例
            driver = webdriver.Chrome(service=service, options=options)

            # 注入 JS 脚本，将 navigator.webdriver 设置为 undefined
            driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
            })

            #把局部driver 赋值给self.driver
            self.driver = driver
            #智能等待，元素是否出现在页面上并且是可见的，最多等待10S。
            self.wait = WebDriverWait(self.driver, 10)

            print("Chrome启动成功！")
            self.logger.info("Chrome启动成功！")

            return self.driver

        except Exception as e:
            self.logger.error(f"浏览器启动失败:{e}",exc_info=True)
            self._cleanup_user_data_dir()
            raise RuntimeError(f"浏览器启动失败: {e}")

    def close_browser(self):
        """关闭浏览器并清理目录"""
        try:
            if self.driver:
                self.driver.quit()
        except Exception as e:
            self.logger.warning(f"关闭浏览器时报错:{e}")
        finally:
            self._cleanup_user_data_dir()

    def _cleanup_user_data_dir(self):
        """仅在并发模式下删除临时目录"""
        if self.parallel and self.user_data_dir and os.path.exists(self.user_data_dir):
            try:
                shutil.rmtree(self.user_data_dir)
                self.logger.info(f"已删除临时用户数据目录: {self.user_data_dir}")
            except Exception as e:
                self.logger.warning(f"删除临时目录失败: {e}",exc_info=True)
        self.user_data_dir = None

