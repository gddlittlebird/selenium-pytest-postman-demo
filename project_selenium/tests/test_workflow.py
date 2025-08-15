import pytest
import logging
from configparser import ConfigParser
from datetime import datetime
from pages.login_page import LoginPage
from pages.forecast_page import ForecastPage
from pages.order_manage_page import OrderManagePage
from pages.cost_fee_page import CostFeePage
from browser_manager import BrowserManager


@pytest.mark.usefixtures("setup")
class TestWorkflow:
    def test_full_workflow(self):
        # 1. 登录
        login_page = LoginPage(self.driver)
        login_page.login()

        # 2. 创建预报单
        forecast_page = ForecastPage(self.driver)
        forecast_page.create_order("John Doe")
        order_id = "TEST123"  # 实际应从页面获取

        # 3. 签收订单
        order_page = OrderManagePage(self.driver)
        order_page.sign_order(order_id)

        # 4. 添加运费
        fee_page = CostFeePage(self.driver)
        fee_page.add_freight("100.00")




##pytest tests/test_workflow.py -n 3 --browser chrome --browser firefox