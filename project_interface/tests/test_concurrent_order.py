import asyncio
import pytest
import httpx
from .testdata import VALID_ACCOUNTS
from .order_payloads import get_order_payload_by_index

# 异步版本的 API 基础 URL，从 pytest fixture 获取
@pytest.fixture(scope="session")
def async_base_url(base_url):
    """
    异步测试用的基础 URL，与同步测试共用 config.yaml 配置。
    """
    return base_url.rstrip("/")


async def async_login_and_order(client: httpx.AsyncClient, base_url: str, account: dict):
    """
    单个用户执行 登录 + 下单 的异步流程。
    参数:
        client: 已创建的 httpx.AsyncClient 对象（支持复用 TCP 连接）
        base_url: API 基础地址
        account: dict，包含 userName, password, order_index 等信息
    """
    # 1. 登录接口
    login_url = f"{base_url}/api/admin/admin-user/login"
    login_payload = {
        "userName": account["userName"],
        "password": account["password"]
    }

    resp_login = await client.post(login_url, json=login_payload)
    assert resp_login.status_code == 200, f"{account['userName']} 登录HTTP状态码错误: {resp_login.status_code}"

    login_json = resp_login.json()
    assert login_json["code"] == account["expected_login_code"], f"{account['userName']} 登录返回code错误: {login_json}"
    assert login_json["message"] == "请求成功", f"{account['userName']} 登录返回message错误: {login_json}"

    login_key = login_json["data"]["loginKey"]
    assert login_key, f"{account['userName']} 登录成功但未返回 loginKey"
    print(f"{account['userName']} 登录成功，loginKey: {login_key}")

    # 2. 下单接口
    order_url = f"{base_url}/api/admin/reserveOrder/create"
    headers = {"loginKey": login_key}
    order_data = get_order_payload_by_index(account["order_index"])

    resp_order = await client.post(order_url, json=order_data, headers=headers)
    assert resp_order.status_code == 200, f"{account['userName']} 下单HTTP状态码错误: {resp_order.status_code}"

    order_json = resp_order.json()
    assert "data" in order_json, f"{account['userName']} 订单返回缺少data字段: {order_json}"
    reserve_order = order_json["data"]["reserveOrder"]
    assert reserve_order and reserve_order.get("innerOrderNo"), f"{account['userName']} 订单返回缺少innerOrderNo: {order_json}"

    print(f"{account['userName']} 下单成功，订单号: {reserve_order['innerOrderNo']}")


@pytest.mark.asyncio
async def test_concurrent_orders(async_base_url):
    """
    并发下单测试：
    - 使用 config.yaml 中的 valid_accounts
    - 每个用户同时执行 登录 + 下单 流程
    - 使用 asyncio.gather 并发运行
    """
    async with httpx.AsyncClient(timeout=10.0) as client:
        tasks = [
            async_login_and_order(client, async_base_url, account)
            for account in VALID_ACCOUNTS
        ]
        await asyncio.gather(*tasks)
