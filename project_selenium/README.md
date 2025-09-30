# Web 自动化测试框架 - Selenium + Pytest

project_selenium/
├── config/                    # 配置文件存放
│   └── config.ini
├── utils/                     # 工具类、公共方法
│   ├── config_manager.py	   # 读取config.ini
│   └── logger.py              # 日志初始化封装
│   └── csv_reader.py          # 读取test中的csv文件
├── core/                      # 核心类（浏览器管理、基类）
│   ├── browser_manager.py     # 
│   └── base_page.py           # 页面公共封装
├── pages/                     # 页面对象模型（POM）
│   ├── login_page.py
│   └── order_page.py
├── tests/                     # 改名更符合 pytest 默认规则
│   ├── test_login.py
│   └── test_order.py
│   └── test_login_performance.py  #测试不同的账户同时登录
│   └── csv files              # 数据准备
│   └── csv files              # 数据准备
├── pytest.ini 				   # 
├── reports/                   # 测试报告存放目录（html/xml等）
├── log/                       # 日志
├── screenshots/               # 截图
├── main.py                    # 可选，通常只做调试时使用
├── requirements.txt
└── README.md                  # 写明依赖、执行命令、结构说明





## 安装依赖
	pip install -r requirements.txt
	
	
pytest test_login_performance.py --alluredir=reports/allure_results









