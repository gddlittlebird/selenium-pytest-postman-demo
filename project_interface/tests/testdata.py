import os
import yaml


ROOT = os.path.dirname(os.path.dirname(__file__))

def load_config():
    """
    加载 config/config.yaml 文件
    返回的是解析后的Python字典，里面包含所有配置
    """

    path = os.path.join(ROOT, "config", "config.yaml")
    with open(path, "r", encoding="utf-8") as f:
        # 使用yaml.safe_load解析YAML文件，返回字典
        return yaml.safe_load(f)

# 缓存变量，避免多次读文件
_config_cache = None

def get_accounts_list(key: str = "accounts"):
    """
    根据传入的key（账号列表的名称）返回对应的账号列表。
    例如：
      - key="accounts" 返回 config.yaml 里 accounts 字段的列表
      - key="valid_accounts" 返回 valid_accounts 列表
    参数:
        key (str): 配置文件中账号列表字段名，默认为"accounts"

    返回:
        list: 账号列表（如果没有找到对应key，返回空列表）

    这个函数会先缓存配置字典，避免多次读取文件，提高效率。
    """
    global _config_cache
    if _config_cache is None:
        # 第一次调用时加载配置文件，后续调用直接复用缓存
        _config_cache = load_config()
    # 从配置字典里获取key对应的账号列表，如果没有该key，返回空列表
    return _config_cache.get(key, [])

# 下面定义两个常用的模块级变量，方便测试代码直接导入使用：
ACCOUNTS = get_accounts_list("accounts")
VALID_ACCOUNTS = get_accounts_list("valid_accounts")
