import platform
import socket
import re
import uuid
import psutil


def getSystemInfo():
    try:
        info = {}
        info['platform'] = platform.system()
        info['platform-release'] = platform.release()
        info['platform-version'] = platform.version()
        info['architecture'] = platform.machine()
        info['hostname'] = socket.gethostname()
        info['mac-address'] = ':'.join(re.findall('..',
                                       '%012x' % uuid.getnode()))
        info['processor'] = platform.processor()
        info['ram'] = str(
            round(psutil.virtual_memory().total / (1024.0 ** 3)))+" GB"
        return info
    except Exception as e:
        print(e)


print(getSystemInfo())
