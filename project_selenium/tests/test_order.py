import pytest
import time
import allure
import os

from utils.csv_reader import load_csv_data
from pages.login_page import LoginPage
from pages.order_page import OrderPage
from utils.config_manager import ConfigManager


@pytest.mark.usefixtures("browser")
@allure.feature("订单模块")  # 大模块分类
class TestOrder:

    @allure.story("创建订单")  # 小场景分类
    @pytest.mark.parametrize("user", load_csv_data("users.csv"))
    def test_create_order(self, user):
        """
        多用户创建预报单测试，使用 CSV 中的数据驱动。
        user 是字典，包含 username、password、customer_name、product_name
        """
        # 给每个测试用例动态标题
        allure.dynamic.title(f"创建订单 - {user['username']}")

        # 初始化页面对象
        login_page = LoginPage(self.driver)
        order_page = OrderPage(self.driver)

        # ================= 登录步骤 =================
        with allure.step(f"用户 {user['username']} 登录"):
            start_time = time.time()
            login_page.login_with_credentials(user["username"], user["password"])
            login_elapsed = time.time() - start_time

            login_ok = login_page.is_welcome_shown(user["username"])
            if login_ok:
                print(f"用户 {user['username']} 登录成功,耗时: {login_elapsed:.2f}秒")
            else:
                # 登录失败时截图并 attach 到 Allure 报告
                screenshot_path = os.path.join(ConfigManager.get_project_dir(), f"{user['username']}_login_fail.png")
                self.driver.save_screenshot(screenshot_path)
                allure.attach.file(screenshot_path, name="登录失败截图", attachment_type=allure.attachment_type.PNG)
                assert False, f"用户 {user['username']} 登录失败"

        # ================= 创建订单步骤 =================
        with allure.step(f"用户 {user['username']} 创建预报单"):
            project_dir = ConfigManager.get_project_dir()
            file_path = os.path.join(project_dir, "tests", "16箱.xlsx")

            start_time = time.time()
            order_page.create_order(
                file_path=file_path,
                customer_name=user["customer_name"],
                product_name=user["product_name"]
            )
            order_elapsed = time.time() - start_time
            print(f"用户 {user['username']} 创建预报单耗时: {order_elapsed:.2f}秒")

            # 可以加断言检查订单是否保存成功
            # if not order_page.is_order_saved_successfully():
            #     screenshot_path = os.path.join(project_dir, f"{user['username']}_order_fail.png")
            #     self.driver.save_screenshot(screenshot_path)
            #     allure.attach.file(screenshot_path, name="创建订单失败截图", attachment_type=allure.attachment_type.PNG)
            #     assert False, "创建订单失败"

if __name__ == '__main__':
    pytest.main([
        "-s",
        "-v",
        "--browser=chrome",
        "--alluredir=reports/allure_results",
        "tests/test_order.py"
    ])
