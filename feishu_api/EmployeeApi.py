from enum import Enum
from feishu_api.ApiBase import client, Method


class EmployeeType(Enum):
    FullTime = 1    # 全职
    Internship = 2  # 实习
    Consultant = 3  # 顾问
    OutSourcing = 4  # 外包
    Laboring = 5    # 劳务


class EmployeeStatus(Enum):
    BeforeJob = 1   # 待入职
    AtJob = 2       # 在职
    DenyJob = 3     # 已取消入职
    BeforeLeave = 4  # 待离职
    Left = 5        # 已离职


class EmployeeInfo(object):
    def __init__(self, data: dict) -> None:
        self.id: str = data["user_id"]  # maybe different id types
        sf: dict = data["system_fields"]
        self.name: str = sf["name"]
        # this file meybe missing ??
        self.department_id: str = str(sf.get("department_id", ""))
        self.employee_type = EmployeeType(int(sf["employee_type"]))
        self.status = EmployeeStatus(int(sf["status"]))


class UserIdType(Enum):
    open_id = "open_id"
    union_id = "union_id"
    user_id = "user_id"


def get_all_employees(id_type: UserIdType = UserIdType.open_id) -> list[EmployeeInfo] | None:
    '''
    返回所有企业员工

    param id_type: EmployeeInfo.id 对应的id类型

    see: https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/ehr/ehr-v1/employee/list
    '''
    l = client.get_all_pages(Method.GET, "open-apis/ehr/v1/employees",
                             query={
                                 "user_id_type": id_type.value
                             })
    if l is None:
        return None
    return [EmployeeInfo(v) for v in l]

# slightly different between user and employy apis
class UserInfo(object):
    def __init__(self, data: dict) -> None:
        self.union_id = data["union_id"]
        self.user_id = data["user_id"]
        self.open_id = data["open_id"]
        self.name = data["name"]
        self.employee_type = EmployeeType(int(data["employee_type"]))


def get_user_by_id(id: str, id_type: UserIdType = UserIdType.open_id) -> UserInfo | None:
    resp = client.request(Method.GET, f"open-apis/contact/v3/users/{id}")
    if resp is None:
        return None
    return UserInfo(resp["user"])


def get_all_user_under_department_id(department_id: str) -> UserInfo | None:
    l = client.get_all_pages(Method.GET, "open-apis/contact/v3/users/find_by_department",
                             query={
                                 "department_id": department_id
                             })
    if l is None:
        return None
    return [UserInfo(v) for v in l]