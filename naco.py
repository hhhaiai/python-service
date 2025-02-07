import json
import socket
import nacos


def get_host_ip():
    res = socket.gethostbyname(socket.gethostname())
    return res


def load_config(content):
    _config = json.loads(content)
    return _config


def nacos_config_callback(args):
    print(args)
    content = args['raw_content']
    load_config(content)


class NacosClient:
    service_name = None
    service_port = None
    service_group = None

    def __init__(self, server_endpoint, namespace_id, username=None, password=None):
        self.client = nacos.NacosClient(server_endpoint,
                                        namespace=namespace_id,
                                        username=username,
                                        password=password,
                                        logLevel="error",   # 只记录错误日志
                                        logDir="/tmp/logs"  # 修改日志目录到 /tmp/logs
                                        )
        self.endpoint = server_endpoint
        self.service_ip = get_host_ip()

    def register(self):
        self.client.add_naming_instance(self.service_name,
                                        self.service_ip,
                                        self.service_port,
                                        group_name=self.service_group)

    def modify(self, service_name, service_ip=None, service_port=None):
        self.client.modify_naming_instance(service_name,
                                           service_ip if service_ip else self.service_ip,
                                           service_port if service_port else self.service_port)

    def unregister(self):
        self.client.remove_naming_instance(self.service_name,
                                           self.service_ip,
                                           self.service_port)

    def set_service(self, service_name, service_ip, service_port, service_group):
        self.service_name = service_name
        self.service_ip = service_ip
        self.service_port = service_port
        self.service_group = service_group

    async def beat_callback(self):
        self.client.send_heartbeat(self.service_name,
                                   self.service_ip,
                                   self.service_port)

    def load_conf(self, data_id, group):
        return self.client.get_config(data_id=data_id, group=group, no_snapshot=True)

    def add_conf_watcher(self, data_id, group, callback):
        self.client.add_config_watcher(data_id=data_id, group=group, cb=callback)


