#test_login_performance.py

import pytest
import allure
import time
from pages.login_page import LoginPage
from utils.csv_reader import load_csv_data

@allure.feature("登录性能测试")
@pytest.mark.parametrize("user_data",load_csv_data("users.csv"))
def test_login_performance(browser,user_data):
    """
    1. 通过参数化读取 CSV 中的多个用户账户和密码。
    2. 使用传入的 browser fixture 启动浏览器实例。
    3. 调用登录页面的 login_with_credentials 方法执行登录。
    4. 记录登录操作的响应时间，方便性能评估。
    5. 登录失败时截图并抛出异常，确保测试失败可追踪。
    """

    login_page = LoginPage(browser)
    username = user_data["username"]
    password = user_data["password"]

    with allure.step(f"开始登录用户，{username}"):
        start_time = time.time()
        try:
            login_page.login_with_credentials(username,password)
        except Exception as e:
            #allure.attach可附加截图到报告
            screenshot_name = f"login_failed_{username}"
            screenshot_path = login_page._take_screenshot(screenshot_name)
            allure.attach.file(
                screenshot_path,
                name=f"{username}登录失败截图",
                attachment_type=allure.attachment_type.PNG
            )
            #抛出异常，使测试用例失败
            login_page.logger.error(f"用户 {username} 登录失败:{str(e)}")
            raise RuntimeError(f"用户登录失败: {username}，错误: {str(e)}") from e

            #pytest.fail(f"用户 {username} 登录失败: {str(e)}")

        end_time = time.time()
        duration = round(end_time - start_time,2)
        login_page.logger.info(f"用户 '{username}'登录耗时：{duration:.2f} 秒")

    with allure.step("记录登录耗时"):
        allure.attach(
            body=f"用户{username} 登录耗时:{duration} 秒",
            name = f"{username} 登录耗时",
            attachment_type=allure.attachment_type.TEXT
        )

    # 性能断言(可根据实际系统性能调整)
    assert duration < 30,f"用户 {username} 登录耗时时长:{duration} 秒"


"""
1. 运行测试 + 生成 Allure 原始结果：
pytest tests/test_login_performance.py --alluredir=reports/allure_results

2. 启动 Allure 服务查看报告：
allure serve reports/allure_results
或生成 HTML 静态报告
allure generate reports/allure_results -o reports/allure_report --clean
allure open reports/allure_report
"""

#pytest -n 1 ./test_login_performance.py
