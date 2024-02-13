import threading
from flask import Flask
from flask import request
import json
import traceback
from nonebot.log import logger
from .ark_record import *

app = Flask(__name__)

@app.route('/record/bind', methods=['GET', 'POST'])
def do_task():
    try: 
        logger.info("【开放API】" + str(request.form))
        msg, code = handle_bind_token(request.form["qq"], request.form["token"])
        return json.dumps({"code": code, "msg": msg, "data": 1})
    except Exception as e:
        err_msg = 'url: %s, err_msg: %s' % (request.url, (str(traceback.format_exc())))
        logger.error(err_msg)
        return json.dumps({"code": 400, "msg": err_msg, "data": 0})

@app.route('/record/test', methods=['GET', 'POST'])
def do_task():
    try: 
      return json.dumps({"code": 200, "msg": "OK", "data": 1})
    except Exception as e:
      return json.dumps({"code": 400, "msg": str(e), "data": 0})


def run_flask():
  logger.info("【开放API】启动中...")
  app.run("0.0.0.0", port=10088)
  logger.info("【开放API】启动完成")
    
flask_thread = threading.Thread(target=run_flask) 
flask_thread.start()
