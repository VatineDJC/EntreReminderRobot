
import json
from log.LoggerSetUp import logger
import typing
from flask import wrappers, request, jsonify
import config
from . import FeishuEvent
from . import _decrypt
import hashlib


class FeishuEventRequest(object):
    def __init__(self, event_id: str, event_type: str, token: str, event: dict) -> None:
        self.event_id = event_id
        self.event_type = event_type
        self.token = token
        self.event = event

    @staticmethod
    def read_from_dict(data: dict[str, typing.Any]):
        event_type: str = ""
        token: str = ""
        event_id: str = ""
        event: dict = data.get("event")

        if "schema" in data:
            # v2
            header: dict = data.get("header")
            event_type = header.get("event_type")
            token = header.get("token")
            event_id = header.get("event_id")
        else:
            # v1
            event_type = event.get("type")
            token = data.get("token")
            event_id = data.get("uuid")

        return FeishuEventRequest(event_id, event_type, token, event)


def feishu_event_handler() -> tuple[str, int] | wrappers.Response:
    '''
    Handler for Feishu Event Http Callback

    [steps]
    - decrypt if needed
    - return to test event
    - check data
    - dispatch events
    '''

    # see: https://open.feishu.cn/document/ukTMukTMukTM/uUTNz4SN1MjL1UzM

    # decrypt data if ENCRYPT is on
    if config.ENCRYPT_KEY != "":
        json_str = _decrypt.AESCipher(
            config.ENCRYPT_KEY).decrypt_string(request.json.get("encrypt"))
        jsobj: dict = json.loads(json_str)
    else:
        jsobj: dict = request.json

    # return to server test event
    if "challenge" in jsobj:
        return jsonify(challenge=jsobj["challenge"])

    req = FeishuEventRequest.read_from_dict(jsobj)
    logger.debug("FeiShu Robot received a request: "+str(req))

    if not _validate_request(req.token):
        logger.error("cannot validate event: "+ str(jsobj))
        return "验证错误", 400

    if _event_repeat_etect(req.event_id):
        logger.warning("repeated event: "+ str(jsobj))
        return "事件重复", 400

    if req.event_type in FeishuEvent._event_map:
        FeishuEvent._event_map[req.event_type](req.event)

    # must return a HTTP:200 (with any body)
    return "OK!", 200


def _validate_request(token: str) -> bool:
    '''
    to check the token and hash in event qequest header

    copy from: https://open.feishu.cn/document/ukTMukTMukTM/uYDNxYjL2QTM24iN0EjN/event-security-verification
    '''

    if token != config.VERIFICATION_TOKEN:
        return False
    timestamp = request.headers.get("X-Lark-Request-Timestamp", "")
    nonce = request.headers.get("X-Lark-Request-Nonce", "")
    signature = request.headers.get("X-Lark-Signature", "")
    body = request.data
    bytes_b1 = (timestamp + nonce + config.ENCRYPT_KEY).encode("utf-8")
    bytes_b = bytes_b1 + body
    h = hashlib.sha256(bytes_b)
    if signature != h.hexdigest():
        return False
    return True


_event_list = []


def _event_repeat_etect(event_id: str) -> bool:
    '''
    该函数用于检测事件是否已经被处理过,请在任意事件处理函数内部使用该该函数来记录event_id以及判定

    see :https://open.feishu.cn/document/ukTMukTMukTM/uUTNz4SN1MjL1UzM
    '''

    global _event_list
    if event_id in _event_list:
        return True
    else:
        _event_list.append(event_id)
        return False
