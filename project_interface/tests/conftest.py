import pytest
import yaml
import os
from src.client_use import ApiClient

ROOT = os.path.dirname(os.path.dirname(__file__))

def load_config():
    """
    以utf-8编码打开文件
    使用yaml.safe_load解析YAML文件为Python字典并返回。
    """
    path = os.path.join(ROOT, "config", "config.yaml")
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

#从文件加载配置，然后把配置保存一份到 pytest 的内部缓存里，方便其它pytest代码快速拿用，最后把配置给调用它的人。
@pytest.fixture(scope="session")
def config(request):
    cfg = load_config()
    #把配置文件的数据临时放到pytest的配置缓存里，方便其他地方（比如动态参数化函数）读取使用。
    request.config._inicache['config_data'] = cfg
    return cfg

@pytest.fixture(scope="session")
def base_url(config):
    #从 config.yaml 里读取 env，如果没写 env 就默认用 dev
    env = config.get("env","dev")
    #从 config.yaml 里读取 base_url 字段（它是个字典）
    base_url_dict = config.get("base_url",{})
    # 根据 env 取对应的 URL，比如 env 是 "dev"，就取 base_url_dict["dev"]
    url = base_url_dict.get(env)
    if not url:
        raise ValueError(f"Base URL not found for env:{env}")
    return url

@pytest.fixture
def api_client(base_url):
    return ApiClient(base_url)
