import pytest
import time
import allure
from utils.csv_reader import load_csv_data
from pages.login_page import LoginPage
from pages.order_page import ForecastPage


@pytest.mark.usefixtures("browser")
class TestOrder:

    @pytest.mark.parametrize("user", load_csv_data("users.csv"))
    def test_create_order(self, user):
        """
        多用户创建预报单测试，使用 CSV 中的数据驱动。
        user 是字典，包含 username、password、customer_name、product_name
        """
        # 1. 登录
        login_page = LoginPage(self.driver)
        start_time = time.time()
        login_page.login_with_credentials(user["username"], user["password"])
        login_elapsed = time.time() - start_time

        assert login_page.is_welcome_shown(user["username"]) is True
        print(f"用户 {user['username']} 登录耗时: {login_elapsed:.2f}秒")

        # 2. 创建预报单
        order_page = ForecastPage(self.driver)
        file_path = r"D:\project_selenium_improve\tests\16箱.xlsx"

        start_time = time.time()
        order_page.create_order(
            file_path=file_path,
            customer_name=user["customer_name"],
            product_name=user["product_name"]
        )
        order_elapsed = time.time() - start_time
        print(f"用户 {user['username']} 创建预报单耗时: {order_elapsed:.2f}秒")

        # 这里可以加断言，例如检查保存成功的提示
        # assert order_page.is_order_saved_successfully()

