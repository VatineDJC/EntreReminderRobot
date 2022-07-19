import feishu_api.ApiBase as ApiBase
import feishu_api.MessageApi as MessageApi
from log.LoggerSetUp import logger
import config
import sys

def im_alive():
    
    config.readConfig()

    client = ApiBase.client
    client.start_token_timer()

    xza = "ou_f2a8336751dea71668ecdbdde035f622"
    cy = 'ou_e63a6350fce767bf370ad1c4cf0f4beb'
    djc = 'ou_be40a94ab52ce8522ed8596f41501249'
    MessageApi.send(MessageApi.MsgRecieverType.User_OpenId, djc, MessageApi.MsgContentType.Text, "【入职提醒机器人】我部署好啦！")
    logger.info("【入职提醒机器人】我部署好啦！")



if __name__ == "__main__":
    im_alive()
