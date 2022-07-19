from enum import Enum
import json
from feishu_api.ApiBase import client, Method

class MsgRecieverType(Enum):
    User_OpenId = "open_id"
    User_UnionId = "union_id"
    User_UserId = "user_id"
    User_Email = "email"
    Group_ChatId = "chat_id"


class MsgContentType(Enum):
    Text = "text"
    Post = "post"

# return: True if success
def send(receive_id_type: MsgRecieverType, receive_id: str, msg_type: MsgContentType, msg: str) -> bool:
    # send message to user, implemented based on Feishu open api capability. doc link: https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/message/create
    query = {
        "receive_id_type": receive_id_type.value
    }
    content: str = ""
    if msg_type == MsgContentType.Text:
        content = json.dumps({"text": msg})
    if msg_type == MsgContentType.Post:
        content = json.dumps(msg)
    req_body = {
        "receive_id": receive_id,
        "content": content,
        "msg_type": msg_type.value,
    }
    resp = client.request(
        Method.POST, "open-apis/im/v1/messages", query=query, body=req_body)
    if resp is None:
        return False
    return True