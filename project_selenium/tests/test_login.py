import pytest
import time
import allure
from utils.csv_reader import load_csv_data
from pages.login_page import LoginPage


#from core.browser_manager import BrowserManager


@pytest.mark.usefixtures("browser")
class TestLogin:

    @pytest.mark.parametrize("user", load_csv_data("users.csv"))
    def test_user_login(self, user):
        """
        多用户登录测试，使用 CSV 中的数据驱动。
        user 是字典，包含 username 和 password
        """
        login_page = LoginPage(self.driver)

        start_time = time.time()
        login_page.login_with_credentials(user["username"], user["password"])
        elapsed = time.time() - start_time

        assert login_page.is_welcome_shown(user["username"]) is True

        print(f"用户 {user['username']} 登录耗时: {elapsed:.2f}秒")

if __name__ == "__main__":
    pytest.main(["-s", "-v", "--browser=chrome", "tests/test_login.py"])
