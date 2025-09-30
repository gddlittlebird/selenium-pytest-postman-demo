import os
import sys
import io
import pytest
import subprocess
from datetime import datetime

# ==================== 解决 Windows 控制台中文乱码 ====================
if os.name == "nt":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    os.system("chcp 65001")  # 设置控制台编码为 UTF-8

# ==================== 配置路径 ====================
project_dir = os.path.dirname(os.path.abspath(__file__))  # 项目根目录
report_dir = os.path.join(project_dir, "reports")         # 报告总目录
allure_results = os.path.join(report_dir, "allure_results")  # Allure 原始数据目录

# 时间戳，用于生成独立的 HTML 报告目录
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
allure_html = os.path.join(report_dir, f"html_{timestamp}")  # HTML 报告目录

# ==================== 运行 pytest ====================
pytest_args = [
    "tests/test_order.py",          # 你的测试文件
    f"--alluredir={allure_results}"  # 指定 Allure 原始数据输出路径
]

# 打印路径方便调试
print(f"Allure 原始数据目录: {os.path.abspath(allure_results)}")
print(f"Allure HTML 报告目录: {os.path.abspath(allure_html)}")

# 执行 pytest
exit_code = pytest.main(pytest_args)

# ==================== 生成 Allure HTML 报告 ====================
# 确保 HTML 报告目录存在
os.makedirs(allure_html, exist_ok=True)

# 使用 subprocess.run 调用 allure.bat，方便捕获报错
allure_cmd = [
    r"D:\allure-2.33.0\bin\allure.bat",
    "generate",
    os.path.abspath(allure_results),
    "-o",
    os.path.abspath(allure_html),
    "--clean"
]

print("\n正在生成 Allure HTML 报告...")
result = subprocess.run(allure_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

# 打印生成报告的输出和错误信息，方便调试
print(result.stdout)
if result.stderr:
    print("生成报告过程中出现错误：")
    print(result.stderr)

# 检查生成是否成功
if result.returncode != 0:
    print("Allure 报告生成失败，请检查 allure 安装和 Java 环境")
else:
    print(f"\nAllure HTML 报告已生成：{allure_html}")

    # ==================== 打开 Allure HTML 报告 ====================
    subprocess.run([
        r"D:\allure-2.33.0\bin\allure.bat",
        "open",
        os.path.abspath(allure_html)
    ])
