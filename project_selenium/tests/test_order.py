import pytest
import time
import allure
import os


from utils.csv_reader import load_csv_data
from pages.login_page import LoginPage
from pages.order_page import OrderPage
from utils.config_manager import ConfigManager


@pytest.mark.usefixtures("browser")
class TestOrder:

    @allure.feature("订单模块")
    @allure.story("创建订单")
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

        # 判断是否登录成功
        login_ok = login_page.is_welcome_shown(user["username"])
        if login_ok:
            print(f"用户 {user['username']} 登录成功,耗时: {login_elapsed:.2f}秒")
        else:
            print(f"用户 {user['username']} 登录失败,耗时: {login_elapsed:.2f}秒")
            assert False, f"用户 {user['username']} 登录失败"

        # 2. 创建预报单
        order_page = OrderPage(self.driver)

        # 3. 上传文件
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

        # 这里可以加断言，例如检查保存成功的提示
        # assert order_page.is_order_saved_successfully()

if __name__ == '__main__':
    pytest.main(["-s", "-v", "--browser=chrome", "tests/test_order.py"])

