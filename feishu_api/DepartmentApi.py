from enum import Enum
from feishu_api.ApiBase import client, Method


class DepartmentInfo(object):
    def __init__(self, data: dict) -> None:
        dept: dict = data["department"]
        self.name: str = dept["name"]
        self.group_id: str = dept["chat_id"]
        self.member_count = int(dept["member_count"])
        self.department_id :str = dept["department_id"]


def info_by_id(department_id: str):
    data = client.request(
        Method.GET, f"open-apis/contact/v3/departments/{department_id}")
    if data is None:
        return None
    return DepartmentInfo(data)
