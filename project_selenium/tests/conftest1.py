import pytest
from browser_manager import BrowserManager

#before pytest 2025/03/13
# def pytest_addoption(parser):
#     parser.addoption("--browser", action="append", default=["chrome"],
#                     help="Browser options: chrome, firefox, edge")
#
# @pytest.fixture(scope="class", params=pytest.config.getoption("--browser"))
# def setup(request):
#     driver = BrowserManager.get_driver(request.param)
#     driver.maximize_window()
#     request.cls.driver = driver
#     yield
#     driver.quit()


#after pytest 2025/03/13
def pytest_addoption(parser):
    # 修正参数定义
    parser.addoption(
        "--browser", #pytest --browser=firefox
        action="store",  # 改为 store 获取单个值
        default="chrome", #直接运行 pytest 等价于 pytest --browser=chrome
        help="Browser options: chrome, firefox, edge" #--browser=BROWSER  Browser options: chrome, firefox, edge
    )


@pytest.fixture(scope="class")  # 作用域设为"class"，整个测试类共享同一个浏览器实例
def browser(request):  # request 是 pytest 内置的上下文对象
    # 获取命令行参数 --browser 的值（如 chrome/firefox）
    browser_name = request.config.getoption("--browser")

    driver = BrowserManager.get_driver(browser_name)
    driver.maximize_window()

    #  将驱动对象传递给测试类（使测试方法中能用 self.driver 操作浏览器）
    request.cls.driver = driver

    # 返回 driver 供测试用例使用
    yield driver

    # 测试类所有用例执行后，退出浏览器（清理资源）
    driver.quit()

@pytest.fixture(params=["chrome", "firefox"])  # 硬编码多浏览器支持
def multi_browser(request):
    """多浏览器参数化方案"""
    driver = BrowserManager.get_driver(request.param)
    driver.maximize_window()
    yield driver
    driver.quit()