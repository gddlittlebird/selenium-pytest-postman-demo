#order_page.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from core.base_page import BasePage
from datetime import datetime
import time


class OrderPage(BasePage):
    """预报单页面操作类"""

    # 元素定位符（类常量）
    FORECAST_ENTRY_BUTTON = (By.XPATH, "(//div[@class='text' and normalize-space(text())='预报|入单'])[1]")
    FORECAST_ORDER_BUTTON = (By.XPATH, '//a[@class="public-small-name" and text()="预报下单"]')
    UPLOAD = (By.XPATH, "//span[text()='点击上传']")
    EXCEL_UPLOAD = (By.XPATH,"//input[@type='file'][@class='el-upload__input'][@accept='.xlsx,.xls']")
    #CUS_ORDER_NUM = (By.XPATH,"//label[text()='客户单号']")
    CUS_NAME = (By.XPATH,"//label[text()='客户名称']//following::input[1]")
    PRODUCT = (By.XPATH, "//label[text()='销售产品']//following::input[1]")
    SAVE = (By.XPATH,"// button[span[text() = '保存']]")
    #CUSTOMER_INPUT = (By.XPATH, "//input[@placeholder='输入客户名称']")  # 假设存在客户名称输入框
    #CUS_OPTION  = (By.XPATH,"//div[@class='el-scrollbar']//span[text()='Customer0222']")
    #PRODUCT_OPTION = (By.XPATH, "//div[@class='el-scrollbar']//span[text()='加拿大海运']")
    LOADING_MASK = (By.CLASS_NAME, "el-loading-mask")
    ORDER_NUM = (By.XPATH,"// p[contains(text(), '客户单号为：')]")

    def _timestamp(self):
        """生成时间戳"""
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    def _get_customer_option_locator(self, customer_name):
        """生成客户选项的动态定位符"""
        return By.XPATH, f"//div[@class='el-scrollbar']//span[text()='{customer_name}']"

    def _get_product_option_locator(self, product_name):
        """生成产品选项的动态定位符"""
        return By.XPATH, f"//div[@class='el-scrollbar']//span[text()='{product_name}']"


    def create_order(self,file_path,customer_name,product_name):
        """
        创建预报单流程
        :param file_path: 上传的Excel文件路径
        :param customer_name: 选择的客户名称
        :param product_name: 选择的销售产品
        """

        self.logger.info(f"开始创建预报单，客户: {customer_name}，产品: {product_name}")

        # 1. 点击预报|入单 （模块处)
        self.click(self.FORECAST_ENTRY_BUTTON,"预报|入单")

        # 2. 点击预报下单
        self.click(self.FORECAST_ORDER_BUTTON,"预报下单")

        # 3.点击上传按钮并上传文件
        try:
            file_input = self.wait.until(EC.presence_of_element_located(self.EXCEL_UPLOAD))

            # 如果 input 被隐藏，先通过 JS 显示
            self.driver.execute_script("arguments[0].style.display = 'block';", file_input)

            file_input.send_keys(file_path)
            self.logger.info(f"上传文件: {file_path}")
        except Exception as e:
            self.handle_error("上传文件失败", e)
            raise

        # 等待遮罩完全消失(优化等待方式)
        try:
            self.wait.until(EC.invisibility_of_element_located(self.LOADING_MASK))
            self.logger.info("文件解析完成，遮罩层已消失")
        except TimeoutException:
            self.logger.warning("等待遮罩层消失超时，可能页面卡住")

        # 4. 输入客户名称并选择
        try:
            cus_name_input = self.wait.until(EC.visibility_of_element_located(self.CUS_NAME))
            cus_name_input.send_keys(customer_name)
            self.logger.info(f"输入客户名称: {customer_name}")

            # 2. 等待下拉选项出现
            target_customer = self.wait.until(
                EC.presence_of_element_located(self._get_customer_option_locator(customer_name))
            )

            # 3. 用 JS 点击下拉选项，保证 Vue 状态更新
            self.driver.execute_script("arguments[0].click();", target_customer)

            self.logger.info(f"选择客户: {customer_name}")
        except Exception as e:
            self.handle_error("输入客户名称并选择", e)
            raise





        # # 4. 输入客户名称并选择
        # self.select_from_dropdown(
        #     input_locator=self.CUS_NAME,
        #     option_locator_func=self._get_customer_option_locator,
        #     value=customer_name,
        #     element_name="客户名称"
        # )

        # 5. 输入销售产品并选择
        self.select_from_dropdown(
            input_locator=self.PRODUCT,
            option_locator_func=self._get_product_option_locator,
            value=product_name,
            element_name="销售产品"
        )

        # 6. 保存提交
        self.click(self.SAVE,"保存")
        try:
            # 等待弹窗出现并定位客户单号元素
            order_element = self.wait.until(EC.visibility_of_element_located(self.ORDER_NUM))
            order_text = order_element.text
            self.logger.info(f"保存成功，客户单号为：{order_text}")
            print(f"保存成功，客户单号为：{order_text}")
            time.sleep(5)
        except Exception as e:
            self.handle_error("保存提交", e)
            raise






