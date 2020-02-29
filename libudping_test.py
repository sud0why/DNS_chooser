import socket
import time
import threading
import json
import random
import string

from timeit import default_timer as timer


def avg(x):
    if len(x) > 0:
        return sum(x) / float(len(x))
    else:
        return


def random_string(length):
    return ''.join(random.choice(string.ascii_letters + string.digits) for m in range(length))


class Socket(object):
    def __init__(self, family, type_, timeout):
        s = socket.socket(family, type_)
        s.settimeout(timeout)
        self._s = s

    def connect(self, host, port=80):
        # self._s.bind((host, int(port)))
        payload = random_string(32)
        self._s.sendto(payload.encode(), (host, port))

    def shutdown(self):
        self._s.shutdown(socket.SHUT_RD)

    def close(self):
        self._s.close()


class Timer(object):
    def __init__(self):
        self._start = 0
        self._stop = 0

    def start(self):
        self._start = timer()

    def stop(self):
        self._stop = timer()

    def cost(self, funcs, args):
        self.start()
        for func, arg in zip(funcs, args):
            if arg:
                func(*arg)
            else:
                func()

        self.stop()
        return self._stop - self._start


class Ping(object):
    def __init__(self, host, port=53, timeout=1):
        self.timer = Timer()

        self._successed = 0
        self._failed = 0
        self._conn_times = []
        self._host = host
        self._port = port
        self._timeout = timeout

    def _create_socket(self, family, type_):
        return Socket(family, type_, self._timeout)

    def ping(self, count=10):
        for n in range(1, count + 1):
            s = self._create_socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                time.sleep(1)
                cost_time = self.timer.cost(
                    (s.connect, s.shutdown),
                    ((self._host, self._port), None))
                s_runtime = 1000 * (cost_time)
                print("%s[:%s]: seq=%d time=%.2f ms" % (self._host, self._port, n, s_runtime))

                self._conn_times.append(s_runtime)
            except Exception as e:
                print(e)
                print("%s[:%s]: seq=%d connect failed" % (self._host, self._port, n))
                self._failed += 1

            else:
                self._successed += 1

            finally:
                s.close()
        return avg(self._conn_times)

    def do_one(self):
        s = self._create_socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            time.sleep(1)
            cost_time = self.timer.cost(
                (s.connect, s.shutdown),
                ((self._host, self._port), None))
            s_runtime = 1000 * (cost_time)
            print("%s[:%s]: time=%.2f ms" % (self._host, self._port, s_runtime))
            return s_runtime

        except:
            print("%s[:%s]: connect failed" % (self._host, self._port))
            return

        finally:
            s.close()


def tcp_do_one(server, port, timeout=1, count=4):
    ping = Ping(server, port, timeout)
    delay = ping.do_one()
    return delay


def tcp_ping(server, port, timeout=1, count=4):
    ping = Ping(server, port, timeout)
    avg_time = ping.ping(count)
    return avg_time


if __name__ == "__main__":
    print(tcp_do_one("114.114.114.114", 53))
    print(tcp_ping("119.29.29.29", 53))
    print(tcp_ping("114.114.114.114", 53))
