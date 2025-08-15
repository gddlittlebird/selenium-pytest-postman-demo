# test_order.py

import pytest
from src.client_use import ApiClient
from .testdata import VALID_ACCOUNTS
from .order_payloads import get_order_payload_by_index


# 用ids参数给每个账号的测试用例起名字，方便测试报告阅读
@pytest.mark.parametrize(
    "account",
    VALID_ACCOUNTS,
    ids=[acc.get("userName") for acc in VALID_ACCOUNTS]
)
def test_order_flow(api_client: ApiClient, account):
    """
    流程化测试用例：
    1. 使用account登录，自动设置loginKey
    2. 生成对应account['order_index']的订单数据，下单
    3. 验证订单返回包含innerOrderNo并打印
    """

    username = account["userName"]
    password = account["password"]
    expected_code = account["expected_login_code"]
    expected_msg = account["expected_data_message"]

    # 登录接口，自动设置 loginKey
    resp_login = api_client.login(username, password)
    login_json = resp_login.json()

    # 断言登录 HTTP 状态码符合预期
    assert login_json["code"] == account[
        "expected_login_code"], f"状态码错误:{login_json['code']} != {account["expected_login_code"]}"

    # 断言登录返回信息符合预期
    assert login_json["message"] == "请求成功", f"{username} 登录返回消息不符"

    # 如果登录成功，loginKey 应该被设置
    assert api_client.login_key is not None, f"{username} 登录成功但 loginKey 未设置"
    print(f"{username} 登录成功，loginKey: {api_client.login_key}")

    # 生成对应订单数据，动态调整产品、国家、用户ID
    order_data = get_order_payload_by_index(account["order_index"])
    #print(f"{username} 生成的订单数据: {order_data}")

    # 创建订单
    order_resp = api_client.create_order(order_data)
    #print(f"{username} 下单返回: {order_resp}")

    # 断言返回数据结构符合预期
    assert "data" in order_resp, f"订单返回缺少data字段，返回内容：{order_resp}"
    reserve_order = order_resp["data"]["reserveOrder"]
    assert reserve_order is not None, f"订单返回缺少reserveOrder字段，返回内容: {order_resp}"
    inner_order_no = reserve_order["innerOrderNo"]
    assert inner_order_no is not None, f"订单返回缺少innerOrderNo,返回内容:{order_resp}"
    print(f"{username} 下单成功，订单号: {inner_order_no}")
