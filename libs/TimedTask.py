'''
用来存放需要与时间相关的指令
WARNING: 默认情况下任务保存在内存,服务重启后任务会消失,
也可将任务保存在各种数据库中(mysql,redis,mongodb)。任务存储进去后,会进行序列化,然后
也可以反序列化提取出来,继续执行。
'''

from enum import Enum
import time
from typing import Callable
from apscheduler.schedulers.background import BackgroundScheduler
from flask_apscheduler import APScheduler
import feishu_api.MessageApi as MessageApi
from log.LoggerSetUp import logger


class JobType(Enum):
    '''
    该类用于区别不同的定时发送任务,类型为JobType
    '''
    WithTime = "message_send_with_time"
    Circularly = "message_send_circularly"


class ExcuteReturn(Enum):
    '''
    该类用于储存不同的函数执行结果返回,类型为ExcuteReturn
    '''
    JOB_SET = "成功设置了新的任务"
    DUE_TIME_PASS = "定时的时间已过期"
    ID_EXIST = "任务设置失败,job_id已存在"
    INVALID_FORMAT = "任务设置失败,请检查命令格式以及时间输入是否正确"
    DELETE_FAIL = "删除任务失败,请检查命令格式以及id输入是否正确"
    ERROR_OCCURED = "发生了错误"
    DELETE_SUCCESS = "成功删除任务"
    HAVE_NO_JOB = "当前无job正在运行"


class TimedTaskClass:
    '''
    该类用于定时任务,具体功能为:
    1. 定时推送消息:message_send_with_time
    2. 循环推送消息:message_send_circularly
    3. 查询任务列表(仅用于聊天用户):job_view
    4. 删除某一任务:delete_job
    5. 删除所有任务:delete_all_job
    使用该类时,不应该实例化使用,请使用timed_task.timeTask
    '''

    def __init__(self) -> None:
        # 用来存放定时任务
        self.timed_task_dic = {}
        self.scheduler = APScheduler(
            BackgroundScheduler(timezone="Asia/Shanghai"))
        self.scheduler.start()

    def _message_send(self, receive_id_type: MessageApi.MsgRecieverType, receive_id: str,
                      content_type: MessageApi.MsgContentType, content: str) -> None:
        '''
        发送信息的函数,向指定id的用户或者群组发送某一类型的消息
        参数表:
        receive_id_type: 接受消息的id的种类,通常有chat_id或open_id
        receive_id: 接受消息的id
        content_type: 发送消息的类型
        content: 发送消息的内容,目前暂时传入str即可
        '''
        if not MessageApi.send(receive_id_type, receive_id, content_type, content):
            logger.error("_message_send() error occured")

    def send_for_with_time(self,job_id: str, receive_id_type: MessageApi.MsgRecieverType, receive_id: str,
                      content_type: MessageApi.MsgContentType, content: str) -> None:
        '''
        专门用于message_send_with_time的函数
        参数表:
        job_id: 定时发送的job_id
        其余参数同_message_send()
        '''
        if not MessageApi.send(receive_id_type, receive_id, content_type, content):
            logger.error("_message_send() error occured")
            return
        self.delete_job_from_dict(job_id)
        

    def test_print(self):
        '''
        用于测试定时模块是否正在运行,目前的测试成功的结果应为输出Log
        '''
        logger.info("This is a test run for timed_task")

    def message_send_with_time(self, job_id: str, receive_id_type: MessageApi.MsgRecieverType, receive_id: str,
                               due_time: str, content_type: MessageApi.MsgContentType, content: str, timezone: str = "Asia/Shanghai") -> ExcuteReturn:
        '''
        该函数用于定时发送消息
        参数表:
        job_id: 任务的id,需要每一个任务均有唯一id
        receive_id_type: 接受消息的id的种类,通常有chat_id或open_id
        receive_id: 接受消息的id
        due_time: 用户设置的定时发送的时间,格式为:"%Y-%m-%d %H:%M:%S"
        content_type: 发送消息的类型
        content:接受消息的内容,目前暂时传入str即可
        timezone: 时区, 默认为"Asia/Shanghai"

        用户输入格式应为: (指令) (job_id) (发送的对象类型) (对象id) (时间) (消息),例如:
        定时发送 job_id_1 用户/群聊 (对应的id) 2022-2-27 22:36:00 发送的消息
        '''
        try:
            try:
                logger.info("send time scheduled in "+str(due_time))
                logger.info(
                    "now_time is " + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))

                # 查看当前定时发送的时间是否过期
                if time.time() - time.mktime(time.strptime(due_time, r"%Y-%m-%d %H:%M:%S")) > 0:
                    logger.info("time passed, job create fail")
                    return ExcuteReturn.DUE_TIME_PASS  # 注意这里有一个return,将会直接结束函数
                else:  # 时间未过期
                    if self.id_exist(job_id):
                        logger.info("id already exist, caused by user")
                        return ExcuteReturn.ID_EXIST  # 查看id是否重合
                    else:  # 设置定时消息
                        self.trigger_date_date(job_id, func=self.send_for_with_time, args=[job_id,
                                               receive_id_type, receive_id, content_type, content], date=due_time, timezone=timezone)
            except:
                return ExcuteReturn.INVALID_FORMAT

            logger.info("New job set successfully(message_send_with_time)")
            # 成功添加了job,将会修改字典
            self.job_dict_insert(job_id, receive_id, content, JobType.WithTime)
            return ExcuteReturn.JOB_SET
        except:
            logger.error("An error occured in message_send_with_time()")
            return ExcuteReturn.ERROR_OCCURED

    def trigger_date_date(self, job_id: str, func: Callable, args: list, date: str, timezone: str) -> None:
        '''
        该函数用于以date为触发器添加一项job
        参数表:
        job_id: 设置的job_id,需要具有唯一性
        func: 定时任务触发时调用的函数
        args: 配套函数的参数
        date: 定时的时间
        timezone: 设置的时区
        '''
        self.scheduler.add_job(id=job_id, func=func, args=args,
                               trigger='date', run_date=date, timezone=timezone)

    def job_dict_insert(self, job_id: str, receive_id: str, content: str, send_type: JobType) -> None:
        '''
        该函数用于向任务字典中插入新任务
        参数表:
        job_id: 对应的job_id
        sender_id: 发送该命令者的open_id
        receive_id: 接受消息的对象的id,通常为open_id或chat_id
        content: 消息的内容
        send_type: 发送的类型
        '''
        if send_type.value not in self.timed_task_dic:
            self.timed_task_dic[send_type.value] = [
                [job_id, receive_id, content]]
        else:
            self.timed_task_dic[send_type.value].append(
                [job_id, receive_id, content])

    def message_send_circularly(self, job_id: str, receive_id_type: MessageApi.MsgRecieverType, receive_id: str,
                                due_time: dict, content_type: MessageApi.MsgContentType, content: str, timezone: str = "Asia/Shanghai") -> ExcuteReturn:
        '''
        该函数用于循环发送消息
        参数表:
        job_id: 任务的id,需要每一个任务均有唯一id
        receive_id_type: 接受消息的id的种类,通常有chat_id或open_id
        receive_id: 接受消息的id
        due_time: 用户设置的定时发送的时间,格式为字典格式
        content_type: 发送消息的类型
        content:接受消息的内容,目前暂时传入str即可
        timezone: 时区,默认为"Asia/Shanghai"
        用户输入格式应为: (指令) (job_id) (发送的对象类型) (对象id) (时间字典) (消息),例如:
        循环发送 job_id 用户/群聊 (对应的id) {"year":(int/str),"month":(int/str),...} 发送的消息
        时间字典(due_time)应获得的格式为字典,参数可不齐备
                参数说明:
                year: 年,4位数字。int 或 str
                month: 月 (范围1-12)。int 或 str
                day: 日 (范围1-31)。int 或 str
                week:周 (范围1-53)。int 或 str
                day_of_week: 周内第几天或者星期几 (范围0-6,0是周一,6是周天 或者 mon,tue,wed,thu,fri,sat,sun)。int 或 str
                hour: 时 (范围0-23)。(int 或 str)
                minute: 分 (范围0-59)。(int 或 str)
                second: 秒 (范围0-59)。(int 或 str)
                start_date: 最早开始日期(包含)。(datetime 或 str)
                end_date: 最晚结束时间(包含)。(datetime 或 str)
                timezone: 指定时区。(datetime 或 str)
        '''
        try:
            try:
                if self.id_exist(job_id):
                    logger.info("id already exist, caused by user")
                    return ExcuteReturn.ID_EXIST  # 查看id是否重合
                else:
                    self.trigger_date_cron(job_id, func=self._message_send, args=[receive_id_type, receive_id,
                                                                                  content_type, content], time=due_time)
            except:
                return ExcuteReturn.INVALID_FORMAT

            logger.info("New job set successfully(message_send_circularly)")
            # 成功添加了job,将会修改字典
            self.job_dict_insert(job_id, receive_id, content, JobType.WithTime)
            return ExcuteReturn.JOB_SET
        except:
            logger.error("An error occured in message_send_circularly()")
            return ExcuteReturn.ERROR_OCCURED

    def trigger_date_cron(self, job_id: str, func: Callable, args: list, time: dict) -> None:
        '''
        该函数用于以crontab为触发器添加一项job
        参数表:
        job_id: 设置的job_id,需要具有唯一性
        func: 定时任务触发时调用的函数
        args: 配套函数的参数
        time: 定时的时间
        '''
        self.scheduler.add_job(id=job_id, func=func,
                               args=args, trigger='cron', **time)

    def id_exist(self, job_id: str) -> bool:
        '''
        该函数为用来查询id是否已经存在
        参数表:
        job_id: 对应的job_id
        '''
        for task_type_list in self.timed_task_dic.keys():
            for task in self.timed_task_dic[task_type_list]:
                if job_id == task[0]:
                    return True
        return False

    def delete_job(self, job_id: str) -> ExcuteReturn:
        '''
        该函数用来根据job_id来删除任务
        参数表:
        job_id: 对应的job_id
        '''
        try:
            self.scheduler.remove_job(job_id)
        except:
            logger.warning("delete_job() failed, may caused by user")
            return ExcuteReturn.DELETE_FAIL
        # 在字典中删除任务
        self.delete_job_from_dict(job_id)
        logger.info("job delete successfully")
        return ExcuteReturn.DELETE_SUCCESS

    def delete_job_from_dict(self,job_id: str) -> None:
        '''
        该函数用来根据job_id在任务记录字典中删除任务
        参数表:
        job_id: 对应的job_id
        '''
        for task_type_list in list(self.timed_task_dic.keys()):
            for task in self.timed_task_dic[task_type_list]:
                if job_id == task[0]:
                    self.timed_task_dic[task_type_list].remove(task)
                    break
            if self.timed_task_dic[task_type_list] == []:
                del self.timed_task_dic[task_type_list]

    def delete_all_job(self) -> ExcuteReturn:
        '''
        该函数用来删除所有job
        '''
        try:
            self.scheduler.remove_all_jobs()
        except:
            logger.warning("delete_all_jobs() failed")
            return ExcuteReturn.DELETE_FAIL
        self.timed_task_dic = {}  # 重置字典
        logger.info("delete_all_jobs() success")
        return ExcuteReturn.DELETE_SUCCESS

    def job_view(self, receive_id) -> ExcuteReturn | None:
        '''
        该函数用于向用户打印job信息
        参数表:
        receive_id: 接受用户的open_id
        '''
        try:
            if self.timed_task_dic == {}:
                return ExcuteReturn.HAVE_NO_JOB
            else:
                self._message_send(MessageApi.MsgRecieverType.User_OpenId, receive_id,
                                   MessageApi.MsgContentType.Text, str(self.timed_task_dic))
                return None
        except:
            logger.error("ERROR: job_view() error occured")
            return ExcuteReturn.ERROR_OCCURED


TimeTask = TimedTaskClass()
