from flask import jsonify
from feishu_api.ApiBase import client, Method

class LoginSession(object):
    def __init__(self, data: dict) -> None:
        self.open_id: str = data["open_id"]
        self.employee_id: str = data["employee_id"]
        pass


def get_login_session(login_token: str) -> LoginSession | None:
    '''
    convert login_toke from miniprog frontend, to id data of feishu user

    see: https://open.feishu.cn/document/uYjL24iN/ukjM04SOyQjL5IDN
    '''
    resp = client.request(Method.POST, "open-apis/mina/v2/tokenLoginValidate",
                          body={"code": login_token})
    if resp is None:
        return None

    return LoginSession(resp)
