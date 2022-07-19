import logging
import config
from libs.events import MessageReceiveEvent, UrlVerificationEvent, EventManager, EmployeeEnterEvent
from feishu_api import MessageApi, DepartmentApi, EmployeeApi
from flask import Flask, jsonify
from libs.PostMsg import get_post_msg


config.readConfig()
event_manager = EventManager()


@event_manager.register("url_verification")
def request_url_verify_handler(req_data: UrlVerificationEvent):
    # url verification, just need return challenge
    if req_data.event.token != config.VERIFICATION_TOKEN:
        raise Exception("VERIFICATION_TOKEN is invalid")
    logging.info(req_data.event.challenge)
    return jsonify({"challenge": req_data.event.challenge})


@event_manager.register("im.message.receive_v1")
def message_receive_event_handler(req_data: MessageReceiveEvent):
    sender_id = req_data.event.sender.sender_id
    message = req_data.event.message
    if event_repeat_etect(req_data.header.event_id):
        logging.warning("repeated event")
        return jsonify()
    if message.message_type != "text":
        logging.warn("Other types of messages have not been processed yet")
        return jsonify()
        # get open_id and text_content
    open_id = sender_id.open_id
    text_content = "你好!   欢迎来到X-Lab！\n" + "Hello！ Welcome to X-Lab!"
    # echo text message
    MessageApi.send(MessageApi.MsgRecieverType.User_OpenId, open_id, MessageApi.MsgContentType.Text, text_content)
    return jsonify()


@event_manager.register("contact.user.created_v3")
def employee_enter_event_handler(req_data: EmployeeEnterEvent):
    if event_repeat_etect(req_data.header.event_id):
        logging.warning("repeated event")
        return jsonify()
    department_info = DepartmentApi.info_by_id(req_data.event.object.department_ids[0])
    employee_info = EmployeeApi.get_user_by_id(req_data.event.object.open_id)
    content = get_post_msg(department_info.name)
    logging.info("send a message to" + employee_info.name + "from" + department_info.name)
    MessageApi.send(MessageApi.MsgRecieverType.User_OpenId, req_data.event.object.open_id,
                    MessageApi.MsgContentType.Post, content)
    return jsonify()


def event_handler():
    # init callback instance and handle
    event_handler, event = event_manager.get_handler_with_event(config.VERIFICATION_TOKEN, config.ENCRYPT_KEY)

    return event_handler(event)


_event_list = []


def event_repeat_etect(event_id: str) -> bool:
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
