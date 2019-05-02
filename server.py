#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio

database = dict()


class ClientServerProtocol(asyncio.Protocol):

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data: bytes):
        cmd = data.decode('utf-8').strip('\n').split(' ')
        self.transport.write(self.data_process(cmd).encode())

    def data_process(self, data):
        if data[0] == 'get':
            return self.get_process(data)
        elif data[0] == 'put':
            return self.put_process(data)
        else:
            return 'error\nwrong command\n\n'

    def get_process(self, get_command):
        resp = 'ok\n'
        if get_command[1] == '*':
            for key, values in database.items():
                for value in values:
                    resp += key + ' ' + value[1] + ' ' + value[0]
        else:
            for value in database[get_command[1]]:
                resp += f'{value[0]} {value[1]}' + '\n'
        resp += '\n'
        return resp

    def put_process(self, put_command):
        if put_command[1] :
            database[put_command[1]] = []
        database[put_command[1]].apend((put_command[2], put_command[3]))
        return 'ok\n\n'


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(ClientServerProtocol, host, port)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()
run_server('127.0.0.1', 8181)
