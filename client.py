#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import socket


class ClientError(BaseException):
    pass


class Client:

    def __init__(self, address, port, timeout=None):
        self._addr = address
        self._port = port
        self._timeout = timeout

    def send(self, cmd):
        with socket.create_connection((self._addr, self._port), self._timeout) as sock:
            sock.sendall(cmd.encode("utf8"))
            buf = sock.recv(1024)
            return buf.decode('utf-8')

    def get(self, key):
        resp = self.send('get ' + key + '\n')
        if resp[0:3] != 'ok\n':
            raise ClientError
        ret = dict()
        lines = resp.split('\n')
        for l in lines[1:-2]:
            metric = l.split(' ')
            res_key = metric[0]
            cpu = float(metric[1])
            timestamp = int(metric[2])
            if not res_key in ret:
                ret[res_key] = []
            ret[res_key].append((timestamp, cpu))
            ret[res_key].sort(key=lambda tup: tup[0])
        return ret

    def put(self, metric, value, timestamp=0):
        resp = self.send('put ' + f'{metric} ' + f'{value} ' + str(timestamp if timestamp else int(time.time())) + '\n')
        if resp[0:3] != 'ok\n':
            raise ClientError
