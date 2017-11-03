#!/usr/bin/env python
# coding=utf-8

import time
import socket, select


EOL1 = b'\n\n'
EOL2 = b'\n\r\n'
response = b'HTTP/1.0 200 OK\r\nDate: Mon, 1 Jan 1996 01:01:01 GMT\r\n'
response += b'Content-Type: text/plain\r\nContent-Length: 13\r\n\r\n'
response += b'Hello, world!'


def create_serversocket(port):
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind(('0.0.0.0', port))
    serversocket.listen(1)

    return serversocket


def create_udpserversocket(port):
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind(('0.0.0.0', port))

    return serversocket


def udp_receice_server(port):
    udp_socket = create_udpserversocket(port)

    while 1:
        data, address = udp_socket.recvfrom(1024)
        print data



def block_server(port=9990):
    serversocket = create_serversocket(port)
    # serversocket.listen(1)

    try:
        while 1:
            print 'waiting...'
            connectiontoclient, address = serversocket.accept()
            request = b''
            while EOL1 not in request and EOL2 not in request:
                request += connectiontoclient.recv(1024)

            print(request.decode())
            connectiontoclient.send(response)
            connectiontoclient.close()
            time.sleep(5)
    finally:
        serversocket.close()


def async_server(port=9991):
    serversocket = create_serversocket(port)
    # socket is default block
    serversocket.setblocking(0)

    # create and register
    epoll = select.epoll()
    # register a read event on serversocket
    epoll.register(serversocket.fileno(), select.EPOLLIN)
    print 'server fileno is [%s]' % serversocket.fileno()
    try:
        connections, requests, responses = {}, {}, {}
        # start polling
        while 1:
            # 1 second timeout
            # print 'polling...'
            events = epoll.poll(1)
            # print events
            # events is a list of tuple (fileno, event)
            for fileno, event in events:
                # server event happend, means a new connection is establishin
                if fileno == serversocket.fileno():
                    # accept and create a new socket for the comming connection
                    client, address = serversocket.accept()
                    client_fileno = client.fileno()
                    print 'accept client by fileno[%s]' % client_fileno
                    # cancel the blocking time
                    client.setblocking(0)
                    # register read event to epoll
                    epoll.register(client_fileno, select.EPOLLIN)
                    # save connection in a list
                    connections[client_fileno] = client
                    requests[client_fileno] = b''
                    responses[client_fileno] = response

                # get a read event(a request)
                elif event & select.EPOLLIN:
                    # get data from socket
                    requests[fileno] += connections[fileno].recv(1024)
                    if EOL1 in requests[fileno] or EOL2 in requests[fileno] or not requests[fileno]:
                        print 'fileno[%s] receive done' % fileno
                        # recv request done, create a write event on epoll
                        epoll.modify(fileno, select.EPOLLOUT)
                        # print recv
                        print('-'*40 + '\n' + requests[fileno].decode()[:-2])

                elif event & select.EPOLLOUT:
                    writtenbytes = connections[fileno].send(responses[fileno])
                    # update remain respone
                    responses[fileno] = responses[fileno][writtenbytes:]
                    # if all response is sent
                    if len(responses[fileno]) == 0:
                        print 'response sent done for fileno[%s]' % fileno
                        epoll.modify(fileno, 0)
                        # tell client to close the connection
                        connections[fileno].shutdown(socket.SHUT_RDWR)
                        # remove
                elif event & select.EPOLLHUP:
                    print 'close fileno[%s] by event[%s]' % (fileno, event)
                    # unregister from epoll
                    epoll.unregister(fileno)
                    # close connection from server side
                    connections[fileno].close()
                    # remove socket fileno from connections list
                    connections.pop(fileno)
                    print 'pop fileno[%s]' % (fileno)
                    print '='*50
    finally:
        # unregister serversocket from epoll
        epoll.unregister(serversocket.fileno())
        # close epoll
        epoll.close()
        # close serversocket
        serversocket.close()


def async_server_edge(port=9992):
    # create server socket
    serversocket = create_serversocket(port)
    serversocket.setblocking(0)

    # create epoll object
    epoll = select.epoll()
    # register read event on server socket(edge mode)
    epoll.register(serversocket.fileno(), select.EPOLLIN | select.EPOLLET)
    try:
        connections, requests, responses = {}, {}, {}
        while 1:
            # poll with 1 second timeout
            events = epoll.poll(1)
            for fileno, event in events:
                # read event from server socket
                if fileno == serversocket.fileno():
                    try:
                        while 1:
                            # get client socket
                            client, address = serversocket.accept()
                            client_fileno = client.fileno()
                            # cancel the blocking time
                            client.setblocking(0)
                            # register read event for client socket(edge mode)
                            epoll.register(client_fileno, select.EPOLLIN | select.EPOLLET)
                            # add to connection list, request list and response list
                            connections[client_fileno] = client
                            requests[client_fileno] = b''
                            responses[client_fileno] = response
                            print 'accept fileno[%s]' % client_fileno
                    except socket.error:
                        print 'accept fileno done'
                        # fetch data from server socket until socket error
                        pass

                # read event
                elif event & select.EPOLLIN:
                    try:
                        while 1:
                            # fetch data from socket
                            requests[fileno] += connections[fileno].recv(1024)
                    except socket.error:
                        # fetch data from socket until socket error
                        pass

                    if EOL1 in requests[fileno] or EOL2 in requests[fileno] or not requests[fileno]:
                        # no data
                        epoll.modify(fileno, select.EPOLLOUT | select.EPOLLET)
                        # print out recv
                        print('-'*40 + '\n' + requests[fileno].decode()[:-2])

                # write event
                elif event & select.EPOLLOUT:
                    try:
                        while 1:
                            # send out response time by time
                            writebytes = connections[fileno].send(responses[fileno])
                            responses[fileno] = responses[fileno][writebytes:]
                    except socket.error:
                        print 'fileno[%s] send done, remain bytes=[%s]' % (fileno, len(responses[fileno]))
                        pass

                    if len(responses[fileno]) == 0:
                        # all data has been sent, clear read/write polling on socket
                        epoll.modify(fileno, select.EPOLLET)
                        # tell the client to close the connection
                        connections[fileno].shutdown(socket.SHUT_RDWR)
                        print 'shutdonw fileno [%s]' % fileno

                elif event & select.EPOLLHUP:
                    # unregister from epoll
                    epoll.unregister(fileno)
                    print 'epoll.unregister(%s)' % fileno
                    connections[fileno].close()
                    print 'connections[%s].close()' % fileno
                    connections.pop(fileno)
                    print 'connections.pop(%s)' % fileno

    finally:
        # unregister serversocket from epoll
        epoll.unregister(serversocket.fileno())
        # close epoll
        epoll.close()
        # close serversocket
        serversocket.close()


if __name__ == '__main__':
    try:
        # block_server()
        # async_server()
        # async_server_edge()
        udp_receice_server(9901)
    except KeyboardInterrupt:
        print 'exit'
    pass
