# API 测试框架 — pytest + requests


本项目基于 `pytest` 实现接口自动化测试，支持多账号登录与下单流程测试。



## 目录结构

api-tests/
├─ config/
│ └─ config.yaml # 环境配置与测试账号（示例，不要提交真实密码）
├─ src/
│ └─ client_use.py # API客户端封装（请求、token管理）
├─ tests/
│ ├─ conftest.py # pytest fixtures（配置加载、客户端初始化）
│ ├─ testdata.py # 从config.yaml加载账号数据，用于参数化测试
│ ├─ order_payloads.py # test_order的数据
│ ├─ test_login.py # 登录接口测试（参数化3个账号）
│ └─ test_order.py # 流程化接口测试（登录-下单-仓库-结算-报表）
├─ requirements.txt # 依赖列表
├─ pytest.ini # pytest配置文件
└─ .github/
└─ workflows/ci.yml # CI（GitHub Actions）配置示例


安装依赖
pip install -r requirements.txt


