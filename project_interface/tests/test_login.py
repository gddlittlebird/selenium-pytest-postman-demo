import pytest
from tests.testdata import ACCOUNTS


#把ACCOUNTS列表里的每个账号对象，依次传给测试函数的参数 account
#ids 用来给每个测试用例命名，方便pytest报告中查看哪个账号失败
@pytest.mark.parametrize("account", ACCOUNTS, ids=[a.get("userName") for a in ACCOUNTS])
def test_login(api_client, account):
    #调用登录接口，拿到响应数据字典
    resp = api_client.login(account["userName"], account["password"])

    json_data = resp.json()
    #HTTP 状态码断言
    assert json_data["code"] == account["expected_login_code"],f"状态码错误:{json_data['code']} != {account["expected_login_code"]}"
    # 顶层message断言
    assert json_data["message"] == "请求成功", f"响应消息不符(顶层message):{json_data['message']}"
    # data.message断言，先确保data存在且有message字段
    assert "data" in json_data and "message" in json_data["data"], f"响应中缺少data.message字段: {json_data}"
    assert json_data["data"]["message"] == account["expected_data_message"], \
        f"响应中data.message不符: {json_data['data']['message']} != {account['expected_data_message']}"