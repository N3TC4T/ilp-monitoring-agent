import os
import multiprocessing
import platform
import datetime
import requests
from .utils import log


def get_accounts():
    try:
        r = requests.get('http://localhost:7769/accounts')
        data = r.json()
    except Exception as err:
        log.error(err)
        data = {}
    return data


def get_routing():
    try:
        r = requests.get('http://localhost:7769/routing')
        data = r.json()
    except Exception as err:
        log.error(err)
        data = {}
    return data


def get_uptime():
    try:
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
            uptime_time = str(datetime.timedelta(seconds=uptime_seconds))
            data = uptime_time.split('.', 1)[0]

    except Exception as err:
        log.error(err)
        data = {}

    return data


def get_load():
    try:
        data = os.getloadavg()[0]
    except Exception as err:
        log.error(err)
        data = {}

    return data

# def get_platform():
#     try:
#         osname = " ".join(platform.linux_distribution())
#         uname = platform.uname()
#
#         if osname == ' ':
#             osname = uname[0]
#
#         data = {'osname': osname, 'hostname': uname[1], 'kernel': uname[2]}
#
#     except Exception as err:
#         log.error(err)
#         data = {}
#     return data

# def get_cpus():
#     try:
#         pipe = os.popen("cat /proc/cpuinfo |" + "grep 'model name'")
#         data = pipe.read().strip().split(':')[-1]
#         pipe.close()
#
#         if not data:
#             pipe = os.popen("cat /proc/cpuinfo |" + "grep 'Processor'")
#             data = pipe.read().strip().split(':')[-1]
#             pipe.close()
#
#         cpus = multiprocessing.cpu_count()
#
#         data = "{CPUS} x {CPU_TYPE}".format(CPUS=cpus, CPU_TYPE=data)
#
#     except Exception as err:
#         log.error(err)
#         data = {}
#
#     return data
#
#
# def get_cpu_usage():
#     try:
#         cpu_pipe = os.popen("iostat").readlines()
#         cpu_res = [line.strip("\n").split() for line in cpu_pipe]
#         cpu_data = cpu_res[3]
#         user_cpu = float(cpu_data[0])
#         nice_cpu = float(cpu_data[1])
#         system_cpu = float(cpu_data[2])
#         iowait_cpu = float(cpu_data[3])
#         steal_cpu = float(cpu_data[4])
#         idle_cpu = float(cpu_data[5])
#
#         usage_cpu = 100.0 - idle_cpu
#
#         cpu_usage_data = {
#             'user_cpu': user_cpu,
#             'nice_cpu': nice_cpu,
#             'system_cpu': system_cpu,
#             'iowait_cpu': iowait_cpu,
#             'steal_cpu': steal_cpu,
#             'idle_cpu': idle_cpu,
#             'usage_cpu': usage_cpu
#         }
#
#         data = cpu_usage_data
#
#     except Exception as err:
#         log.error(err)
#         data = {}
#
#     return data
#
#
# def get_mem():
#     try:
#         mem_pipe = os.popen("free -m").readlines()
#         if len(mem_pipe) == 3:
#             mem_res = [line.strip("\n").split() for line in mem_pipe]
#             total_mem = int(mem_res[1][1])
#             total_used = int(mem_res[2][2])
#             total_free = int(mem_res[2][3])
#             swap_total = 0
#             swap_used = 0
#             swap_free = 0
#             percent = (100 - ((total_free * 100) / total_mem))
#         elif len(mem_pipe) == 4:
#             mem_res = [line.strip("\n").split() for line in mem_pipe]
#             total_mem = int(mem_res[1][1])
#             total_used = int(mem_res[2][2])
#             total_free = int(mem_res[2][3])
#             swap_total = int(mem_res[3][1])
#             swap_used = int(mem_res[3][2])
#             swap_free = int(mem_res[3][3])
#             percent = (100 - ((total_free * 100) / total_mem))
#         else:
#             total_mem = 0
#             total_used = 0
#             total_free = 0
#             swap_total = 0
#             swap_used = 0
#             swap_free = 0
#             percent = 0
#
#         mem_usage = {'total': total_mem,
#                      'usage': total_used,
#                      'free': total_free,
#                      'swap_total': swap_total,
#                      'swap_used': swap_used,
#                      'swap_free': swap_free,
#                      'percent': percent}
#
#         data = mem_usage
#
#     except Exception as err:
#         log.error(err)
#         data = {}
#
#     return data
