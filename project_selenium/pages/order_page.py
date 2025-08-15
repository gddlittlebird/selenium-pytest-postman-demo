from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from core.base_page import BasePage
import time


class ForecastPage(BasePage):
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
        try:
            self.wait.until(EC.element_to_be_clickable(self.FORECAST_ENTRY_BUTTON)).click()
            self.logger.info("点击 预报|入单按钮")
        except Exception as e:
            self.logger.error(f"预报|入单 模块 失败: {e}")
            self._take_screenshot("预报入单_page_failed")
            raise

        # 2. 点击预报下单
        try:
            self.wait.until(EC.element_to_be_clickable(self.FORECAST_ORDER_BUTTON)).click()
            self.logger.info("点击 预报下单按钮，进入预报下单页面")
        except Exception as e:
            self.logger.error(f"进入预报下单 页面 失败: {e}")
            self._take_screenshot("Enter_forecast_order_page_failed")
            raise

        # 3.点击上传按钮并上传文件
        try:
            #self.wait.until(EC.element_to_be_clickable(self.UPLOAD)).click()
            #file_input = self.wait.until(EC.presence_of_element_located(self.EXCEL_UPLOAD))

            file_input = self.wait.until(EC.presence_of_element_located(self.EXCEL_UPLOAD))

            # 如果 input 被隐藏，先通过 JS 显示
            self.driver.execute_script("arguments[0].style.display = 'block';", file_input)

            file_input.send_keys(file_path)
            self.logger.info(f"上传文件: {file_path}")
        except Exception as e:
            self.logger.error(f"上传文件失败: {e}")
            self._take_screenshot("step_upload_file_failed")
            raise

        try:
            self.wait.until_not(EC.presence_of_element_located(self.LOADING_MASK))
            self.logger.info("文件解析完成，遮罩层已消失")
        except TimeoutException:
            self.logger.warning("等待遮罩层消失超时，可能页面卡住")

        # 4. 输入客户名称并选择
        try:
            cus_name_input = self.wait.until(EC.presence_of_element_located(self.CUS_NAME))
            cus_name_input.send_keys(customer_name)
            self.logger.info(f"输入客户名称: {customer_name}")

            target_customer = self.wait.until(
                EC.element_to_be_clickable(self._get_customer_option_locator(customer_name)))
            target_customer.click()
            self.logger.info(f"选择客户: {customer_name}")
        except Exception as e:
            self.logger.error(f"选择客户失败: {e}")
            self._take_screenshot("step_select_customer_failed")
            raise

        # 5. 输入销售产品并选择
        try:
            product_input = self.wait.until(EC.presence_of_element_located(self.PRODUCT))
            product_input.send_keys(product_name)
            self.logger.info(f"输入客户: {customer_name}的销售产品{product_name}")

            target_product = self.wait.until(
                EC.element_to_be_clickable(self._get_product_option_locator(product_name)))
            target_product.click()
            self.logger.info(f"选择销售产品: {product_name}")
        except Exception as e:
            self.logger.error(f"选择销售产品失败: {e}")
            self._take_screenshot("step_select_product_failed")
            raise

        # 6. 保存提交
        try:
            save_submit = self.wait.until(EC.element_to_be_clickable(self.SAVE))
            save_submit.click()
            self.logger.info("保存并提交预报单")

            # 等待弹窗出现并定位客户单号元素
            order_element = self.wait.until(EC.presence_of_element_located(self.ORDER_NUM))
            order_text = order_element.text
            self.logger.info(f"保存成功，客户单号为：{order_text}")
            print(f"保存成功，客户单号为：{order_text}")
            time.sleep(5)
        except Exception as e:
            self.logger.error(f"保存提交失败: {e}")
            self._take_screenshot("step_save_order_failed")
            raise


