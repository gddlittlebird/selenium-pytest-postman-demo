# config_manager.py

import os
import logging
from configparser import ConfigParser


"""
    ConfigManager 是一个单例类（只创建一个实例）：
    - 它的作用是读取 config.ini 文件中的配置项
    - 自动创建项目需要的目录（如 logs、screenshots）
    - 配置日志系统（记录测试信息）
"""


class ConfigManager:
    """配置管理（单例模式）
    ConfigManager 使用单例模式加载和管理配置文件及相关路径，确保系统全局统一读取配置。
    同时负责创建必要的目录结构和初始化日志系统。

    易懂版：
    # 作用：确保整个程序中只有一个配置管理器（就像公司唯一的行政主管）
    # 类比：无论多少部门要申请物资，都找同一个行政主管，避免重复创建资源
    """

    _instance = None
    logger_initialized = False  # 防止重复初始化日志

    def __new__(cls):
        """
        每次创建对象前，都会调用它。我们在这里实现“单例”逻辑：
        如果已经存在实例，直接返回；
        如果没有，就创建新实例。
        """
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._init_config() #初始化配置，路径和日志
        return cls._instance

    def _init_config(self):
        """
        初始化步骤(程序启动时只运行一次)：
        1.加载配置文件
        2.定义并创建项目目录(config,logs,screenshots)
        3.设置日志记录功能
        """
        self.config = ConfigParser()
        self.logger = logging.getLogger(__name__)

        #当前文件所在目录
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        #项目根目录
        self.project_dir = os.path.abspath(os.path.join(self.current_dir, ".."))
        #配置文件目录
        self.config_dir = os.path.join(self.project_dir, "config")
        #配置文件完整路径
        self.config_file = os.path.join(self.config_dir, "config.ini")
        #截图目录
        self.screenshots_dir = os.path.join(self.project_dir, "screenshots")
        #日志目录
        self.log_dir = os.path.join(self.project_dir,"logs")

        # 存储所有需要创建的目录
        self.directories = {
            "config": self.config_dir,
            "screenshots": self.screenshots_dir,
            "logs": self.log_dir,
        }

        # 创建目录
        self._create_directories()
        #初始化日志
        self._init_logger()
        #加载配置文件
        self._load_config()

    def _create_directories(self):
        """
        创建程序运行所需要的所有目录(如果目录已经存在，会自动跳过)
        """
        for directory in self.directories.values():
            try:
                os.makedirs(directory, exist_ok=True)
                self._log(f"目录已创建或已存在: {directory}", level=logging.INFO)
            except OSError as e:
                self._log(f"目录创建失败: {str(e)}", level=logging.CRITICAL)
                #RuntimeError 无特定分类，但运行中发现逻辑错误
                raise RuntimeError(f"创建目录失败:{directory}.信息错误：{e}")

    def _init_logger(self):
        """
        - 把日志写入文件 manual_test.log
        - 格式包括时间,模块名，日志级别和内容
        """
        #防止重复添加日志处理器
        if not ConfigManager.logger_initialized:
            log_file = os.path.join(self.log_dir, 'manual_test.log')

            # 防止重复添加日志处理器
            if not self.logger.handlers:
                # 创建一个日志处理器
                file_handler = logging.FileHandler(log_file, encoding='utf-8')
                # 设置日志格式
                formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
                file_handler.setFormatter(formatter)

                self.logger.addHandler(file_handler)
                self.logger.setLevel(logging.INFO)

                # 日志系统初始化成功
                self._log("日志系统初始化成功")

                # 标记日志系统已经初始化
                ConfigManager.logger_initialized = True


    def _load_config(self):
        """
        加载配置文件(config.ini)内容
        -如果找不到配置文件，会记录warning
        -如果读取失败，会抛出错误
        """

        if os.path.exists(self.config_file):
            try:
                self.config.read(self.config_file,encoding="utf-8")
                self._log(f"配置文件已加载:{self.config_file}")
            except Exception as e:
                #打印日志记录错误信息
                self._log(f"配置文件解析失败：{str(e)}",level=logging.ERROR)
                #把原来的异常继续跑出去
                raise
        else:
            self._log(f"配置文件未找到：{self.config_file}",level=logging.WARNING)


    def _log(self, message, level=logging.INFO):
        self.logger.log(level, message)

    # ---------- 公共方法 ----------
    @classmethod
    def get_from_config(cls, section, option, default=None):
        """安全获取配置项（支持默认值）"""
        instance = cls()
        try:
            return instance.config.get(section, option)
        except Exception as e:
            instance._log(f"读取配置 {section}.{option}失败，使用默认值 {default}。错误:{e}", level=logging.WARNING)
            return default

    @classmethod
    def get_project_dir(cls) -> str:
        """获取项目根目录"""
        return cls().project_dir

    @classmethod
    def get_screenshots_dir(cls) -> str:
        """获取截图目录"""
        return cls().screenshots_dir

    @classmethod
    def get_log_dir(cls) -> str:
        """获取日志目录"""
        return cls().log_dir

    @classmethod
    def get_log_file(cls) -> str:
        """获取日志文件路径"""
        return os.path.join(cls.get_log_dir(), "manual_test.log")