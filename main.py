from log.LoggerSetUp import logger
import plugins.xlab_server.routes as xlab_routes
import robot_server.routes as feishu_routes
import feishu_api.ApiBase as ApiBase
from apscheduler.schedulers.blocking import BlockingScheduler
import config
from flask import Flask, jsonify
import sys


sys.path.append(".")
sys.path.append("..")


'''
The server is both used to 
listen Feishu Events & handle xlab requests
handlers are recommended to save in ../plugin
'''

app = Flask(__name__)


@app.get("/api/ping")
def echo():
    return "pong"


def main():
    
    logger.info("Robot start up")
    config.readConfig()

    client = ApiBase.client
    client.start_token_timer()

    feishu_routes.register(app)
    xlab_routes.register(app)

    app.run(host='0.0.0.0', port=config.PORT, debug=False, threaded=True, use_reloader=False)


if __name__ == "__main__":
    main()
