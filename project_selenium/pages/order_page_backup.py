from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from core.base_page import BasePage


class ForecastPage(BasePage):
    """预报单页面操作类"""

    # 元素定位符（类常量）
    FORECAST_ENTRY_BUTTON = (By.XPATH, "(//div[@class='text' and normalize-space(text())='预报|入单'])[1]")
    FORECAST_ORDER_BUTTON = (By.XPATH, '//a[@class="public-small-name" and text()="预报下单"]')
    UPLOAD = (By.XPATH, "//span[text()='点击上传']")
    EXCEL_UPLOAD = (By.XPATH,"//input[@type='file'][@class='el-upload__input'][@accept='.xlsx,.xls']")
    CUS_ORDER_NUM = (By.XPATH,"//label[text()='客户单号']")
    CUS_NAME = (By.XPATH,"//label[text()='客户名称']//following::input[1]")
    PRODUCT = (By.XPATH,"//label[text()='销售产品']//following::input[1]")
    CUSTOMER = (By.XPATH,"//div[@class='el-scrollbar']//span[text()='Customer0222']")

    #CUSTOMER_INPUT = (By.XPATH, "//input[@placeholder='输入客户名称']")  # 假设存在客户名称输入框

    def create_order(self):
        """
        创建预报单流程
        :param file_path: 上传的Excel文件路径
        :param customer_name: 选择的客户名称
        """
        try:
            # wait = WebDriverWait(self.driver,10)
            # self.logger.info("开始创建预报单")

            self.click(self.FORECAST_ENTRY_BUTTON,"预报|入单")
            sleep(1)
            self.click(self.FORECAST_ORDER_BUTTON, "预报下单")
            sleep(1)

            self.click(self.UPLOAD, "点击上传")
            sleep(1)


            #上传文件
            file_input = self.wait.until(EC.presence_of_element_located(self.EXCEL_UPLOAD))
            file_path = r"D:\PythonProject1\test_files\YC250219014_test.xlsx"  # 替换为实际文件路径
            file_input.send_keys(file_path)
            sleep(3)

            #清除客户单号
            cus_num = self.wait.until(EC.element_to_be_clickable(self.CUS_ORDER_NUM))
            cus_num.clear()
            sleep(3)

            #选择客户名称
            input_customer_box = self.wait.until(EC.EC.presence_of_element_located(self.CUS_NAME))
            input_customer_box.send_keys("Customer0222")  # 输入模糊文本
            sleep(1)  # 等待下拉选项加载
            # 定位下拉选项并选择目标选项
            target_customer = self.wait.until(EC.EC.element_to_be_clickable(self.CUSTOMER))
            target_customer.click()  # 点击选择目标选项
            print("已选择客户: Customer0222")


            #选择销售产品


            #保存







            # print(f"已上传文件: {file_path}")
            #
            # # Step 3: 输入客户名称（根据实际页面逻辑扩展）
            # # self.input_text(self.CUSTOMER_INPUT, customer_name, "客户名称输入框")
            # # self.logger.info(f"已输入客户名称: {customer_name}")
            #
            # # 其他操作（如提交表单）可在此扩展...
            #
            # self.logger.info("预报单创建流程完成")

        except Exception as e:
            self.logger.error(f"创建预报单失败: {str(e)}")
            self._take_screenshot("forecast_order_failed")
            raise

