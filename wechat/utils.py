from functools import wraps
import signal
import time
import os


def time_limit(interval):
    def deco(func):
        def signal_handler(signum, frame):
            raise Exception("Timed out!")

        @wraps(func)
        def deco(*args, **kwargs):
            signal.signal(signal.SIGALRM, signal_handler)
            signal.alarm(interval)
            try:
                return func(*args, **kwargs)
            except:
                return "time out"
        return deco
    return deco

def check_pid(pid):
    try:
        os.kill(pid,0)
    except:
        return False
    else:
        return True

def myTry(func):
    @wraps(func)
    def deco(*args, **kwargs):
        try:                
            return func(*args, **kwargs)
        except:
            return "出现错误，请重试"
    return myTry

def killProcess(pid):
    try:
        os.kill(pid, signal.SIGKILL)
    except:
        pass