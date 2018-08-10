#!/usr/bin/env python
# coding: utf-8

import socket
import time
import json
import pkg_resources
from requests import Session
from requests.exceptions import ConnectionError

from .lib import utils, daemon, collectors


class NSConf:
    def __init__(self):
        self.server_ip = utils.get_conf_pat("server", "ip")
        self.server_port = utils.get_conf_pat("server", "port")
        self.agent_interval = utils.get_conf_pat("agent", "interval")


class InfoGather:

    def __init__(self):
        self.agent_data = dict()
        self.now_capture_time = int(time.time())
        self.hostname = socket.gethostname()
        self.agent_version = pkg_resources.get_distribution("ilp_monitoring_agent").version
        try:
            csock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            csock.connect(('8.8.8.8', 80))
            (addr, port) = csock.getsockname()
            csock.close()
            self.ip = addr
        except socket.error:
            self.ip = '127.0.0.1'

        self.agent_data['agent_version'] = self.agent_version
        self.agent_data['hostname'] = self.hostname
        self.agent_data['ip'] = self.ip
        self.agent_data['capture_time'] = self.now_capture_time

    def run_all_collectors(self):
        for collector in dir(collectors):
            func = getattr(collectors, collector)
            if callable(func):
                self.agent_data[func.__name__.split('_')[1]] = func()
        return self.agent_data


class DataDelivery(Session):
    def __init__(self):
        super(DataDelivery, self).__init__()
        self.max_retry = 3

    def __recoverable(self, error, url, request, counter=1):
        if hasattr(error, 'status_code'):
            if error.status_code in [502, 503, 504]:
                error = "HTTP %s" % error.status_code
            else:
                return False
        if counter > self.max_retry:
            return False
        DELAY = 10 * counter
        utils.log.error("Got recoverable error [%s] from %s %s, retry #%s in %ss" % (error, request, url, counter, DELAY))
        time.sleep(DELAY)
        return True

    def post(self, url, **kwargs):
        counter = 0
        while True:
            counter += 1
            try:
                r = super(DataDelivery, self).post(url, **kwargs)
            except ConnectionError as e:
                if hasattr(e, 'message'):
                    r = e.message
                else:
                    r = e
                if self.__recoverable(r, url, 'POST', counter):
                    continue
                else:
                    raise Exception("Failed sending data to server after %s tries , abort sending..." % self.max_retry)
            return r


class AgentDaemon(daemon.Daemon):
    def run(self):
        apm = NSConf()
        while True:
            ig = InfoGather()
            info_data = ig.run_all_collectors()
            try:
                delivery = DataDelivery()
                delivery.post("http://{IP}:{PORT}/api/agent".format(IP=apm.server_ip, PORT=apm.server_port),
                                    json=json.dumps(info_data))
            except Exception as e:
                utils.log.error(e)
            time.sleep(int(apm.agent_interval))