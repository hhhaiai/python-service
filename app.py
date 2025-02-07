from flask import Flask, request, jsonify
import google_translation as gt
import naco
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import atexit
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
# from prometheus_client import Counter, start_http_server
import configparser
import os
import json


app = Flask(__name__)  # 基本初始化，参数只接受import_name等标准参数

# 使用app.config存储版本信息和描述
app.config['VERSION'] = "1.0.6|2025.2.7"
app.config['DESCRIPTION'] = "High-performance API service"

# 确保 JSON 响应不使用 ASCII 编码
app.json.ensure_ascii = False

executors = {
    'default': ThreadPoolExecutor(1),
    'processpool': ProcessPoolExecutor(1)
}

job_defaults = {
    'coalesce': False,
    'max_instances': 5
}


def read_config_section_to_dict( section='SERVER'):
    """
    正式环境 section='SERVER'
    测试环境 section='TEST'
    本地环境 section='LOCAL'
    海外环境 section='ABROAD'
    """
    config = json.loads(os.getenv('ENV_CONFIG'))
    default_section = config[section]
    # 将DEFAULT部分的内容转换为列表
    re_dict = {}
    for key, value in default_section.items():
        re_dict[key] = value
    # default_list = [(key, value) for key, value in default_section.items()]
    return re_dict


try:
    _config = read_config_section_to_dict()
except BaseException as e:
    _e = e
    _config = {}

SERVER_ADDRESSES = _config.get('nacos_host', "")  # Nacos 服务器地址
NAMESPACE = ""  # 使用的命名空间，可以为空，表示使用默认命名空间
SERVICE_NAME = _config.get('nacos_service_name', "")  # 注册到 Nacos 的服务名称
GROUP_NAME = _config.get('nacos_group_name', "")  # 服务所属的组
IP = _config.get('server_host', "")  # 服务的 IP 地址
PORT = int(_config.get('server_port', 443))  # 服务的端口号

# ERROR_COUNTER = Counter('http_500_errors_total', 'Total number of HTTP 500 errors')
ERROR_COUNT = 0

def beat_callback():
    _t = gt.health()
    client.client.add_naming_instance(
        SERVICE_NAME, IP, PORT, cluster_name="DEFAULT", group_name=GROUP_NAME, ephemeral=True, metadata={"heartbeat_interval": "5"}
    )


if SERVER_ADDRESSES:
    scheduler = BackgroundScheduler(executors=executors, job_defaults=job_defaults)
    client = naco.NacosClient(SERVER_ADDRESSES, NAMESPACE)

    beat_callback()
    scheduler.add_job(
        func=beat_callback,
        trigger=IntervalTrigger(seconds=7),
        id='example_job',
        name='示例任务',
        replace_existing=True
    )

    if not scheduler.running:
        scheduler.start()

    atexit.register(lambda: scheduler.shutdown())


@app.route('/translate', methods=['POST'])
def translate():
    global ERROR_COUNT
    if ERROR_COUNT > 5:
        shutdown()
    try:
        _data = request.get_json()
        re_data = gt.translate(_data)
        if re_data['code'] == 500:
            ERROR_COUNT += 1
            return {'code': 500, 'message': f'error: google code 500'}
        ERROR_COUNT = 0
        return re_data
    except Exception as e:
        ERROR_COUNT += 1
        return {'code': 500, 'message': f'error: {e}'}

@app.route('/version')
def get_version():
    """返回当前服务版本号"""
    return jsonify({
        "service": "gugu",
        "version": app.config['VERSION']
    })

@app.route('/health', methods=['GET'])
def health():
    global ERROR_COUNT
    if ERROR_COUNT > 5:
        shutdown()
    try:
        _t = gt.health()

        if _t >= 0:
            ERROR_COUNT = 0
            return jsonify({"status": "healthy"}), 200   # {"code": "200", "message": "success", "data": f"{_t}"}
        else:
            ERROR_COUNT += 1
            return jsonify({"code": 500, "message": "fail", "data": f"{_t}"}), 500
    except Exception as e:
        # ERROR_COUNTER.inc()
        return jsonify({'error': str(e)})


def shutdown():
    # 获取 Flask 服务器的 `werkzeug.server.shutdown` 函数
    func = request.environ.get('werkzeug.server.shutdown')

    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')

    # 关闭服务器
    func()
    return 'Server shutting down...'



if __name__ == '__main__':
    # start_http_server(CHECK_PORT)
    app.run(debug=False, host='0.0.0.0', port=os.getenv('PORT',7860))

