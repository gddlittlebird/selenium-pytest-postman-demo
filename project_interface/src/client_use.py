import requests
from typing import Optional, Dict, Any

class ApiClient:
    """
    简单API客户端：
    - 管理base_url
    - 请求封装get/post,自动带上loginKey
    - 登录接口获取 loginkey
    """

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.login_key: Optional[str] = None
        self.session.headers.update({
            "content-type":"application/json; charset=utf-8"
        })

    def _full_url(self, path: str) -> str:
        if path.startswith('/'):
            return f"{self.base_url}{path}"
        return f"{self.base_url}/{path}"

    def set_login_key(self, login_key: str):
        self.login_key = login_key
        self.session.headers.update({"loginKey": login_key})

    def get(self, path: str, **kwargs) -> requests.Response:
        url = self._full_url(path)
        return self.session.get(url, **kwargs)

    def post(self, path: str, json: Optional[Dict[str, Any]] = None, **kwargs) -> requests.Response:
        url = self._full_url(path)
        return self.session.post(url, json=json, **kwargs)


    #业务接口测试
    def login(self,username,password):
        payload = {"userName": username, "password": password}
        resp = self.post("/api/admin/admin-user/login", json=payload)
        print("登录接口返回：", resp.status_code, resp.text)  # 调试用
        resp.raise_for_status()
        data = resp.json()
        login_key = data.get("data",{}).get("loginKey")
        if login_key:
            self.set_login_key(login_key)
        return resp

    def create_order(self,order_data):
        resp = self.post("/api/admin/reserveOrder/create",json=order_data)
        resp.raise_for_status()
        return resp.json()


