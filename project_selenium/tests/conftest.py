import os
import pytest
from xdist.plugin import worker_id
from core.browser_manager import BrowserManager
from utils.csv_reader import load_csv_data


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="append",
        default="chrome",
        help="Browser option: chrome, firefox, edge"
    )

@pytest.fixture(scope="class")
def browser(request):
    browser_name = request.config.getoption("--browser")
    manager = BrowserManager(parallel=False)
    driver = manager.start_browser(browser_type=browser_name)
    request.cls.driver = driver
    yield driver
    manager.close_browser()


# @pytest.fixture(scope="class")
# def setup(request):
#     driver = BrowserManager.get_driver(request.param)
#     driver.maximize_window()
#     request.cls.driver = driver
#     yield
#     driver.quit()






# 并发用
# @pytest.fixture
# def browser(request):
#     #用户手动传 --parallel 则优先启用并发模式
#     parallel = request.config.getoption("--parallel")
#
#     #如果 pytest-xdist运行时，worker 数 > 1 才自动启用并发模式
#     worker_id = os.environ.get("PYTEST_XDIST_WORKER")
#     total_workers = os.environ.get("PYTEST_XDIST_WORKER_COUNT")
#
#     # 2. 如果没传 --parallel，但 pytest-xdist 在运行（说明是 -n 并发），也自动启用并发模式
#     #if not parallel and os.environ.get("PYTEST_XDIST_WORKER"):
#     if not parallel and worker_id and total_workers and int(total_workers)>1:
#         parallel = True
#
#     manager = BrowserManager(parallel=parallel)
#     driver = manager.start_browser()
#     yield driver
#     manager.close_browser()
#
# def pytest_addoption(parser):
#     parser.addoption("--parallel", action="store_true", help="启用并发模式")
