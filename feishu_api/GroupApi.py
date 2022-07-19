from feishu_api.ApiBase import client, Method


class GroupInfo(object):
    '''not every item in json are included, cuz some are useless'''

    def __init__(self, obj: dict):
        self.ChatId = str(obj.get("chat_id"))
        self.Name = str(obj.get("name"))
        self.TenantKey = str(obj.get("tenant_key"))


def get_group_list() -> list[GroupInfo] | None:
    '''
    Note: length of list return <= 100
    return None if fail
    '''
    # see: https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/chat/list

    l = client.get_all_pages(Method.GET, "open-apis/im/v1/chats")
    if l is None:
        return None
    return [GroupInfo(v) for v in l]


class GroupMember(object):
    def __init__(self, data: dict[str, str]) -> None:
        self.open_id: str = data["member_id"]
        self.name: str = data["name"]


def get_group_members(group_id: str) -> list[GroupMember] | None:
    '''
    Note: length of list return <= 100
    return None if fail
    '''
    l = client.get_all_pages(
        Method.GET, f"open-apis/im/v1/chats/{group_id}/members", body={"member_id_type": "open_id"})
    if l is None:
        return None
    
    return [GroupMember(v) for v in l]
