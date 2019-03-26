# from Codes import Code
import byteutil
import traceback
import socket
# import timeout_decorator


def newUDPSocket():
    return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def newTCPSocket():
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def reprTCPSocket(sock):
    closed = getattr(sock, '_closed', False)
    return "<{}{} --> {}>".format(
        "[closed] " if closed else "",
        sock.getsockname(),
        sock.getpeername()
    )


def reprSocketServer(sockserv):
    return "<(SocketServer listening on {sock})>".format(
        sock=sockserv.socket.getsockname()
    )


def getOwnIP():
    return ''
    # for addrinfo in socket.getaddrinfo(socket.gethostname(), 0):
    #     family, __, __, __, address = addrinfo
    #         if family == socket.AddressFamily.AF_INET:
    #             return address[0]


def sendUDP(sock, bytesmsg, dest_address):
    if SHOW_NET_INFO:
        print("┌ Sending UDP message")
        print("│ Server: {}:{}".format(*dest_address))
        print("│ ┌Message (bytes): '{}'".format(bytesmsg))
        print("└ └Message (print): {}".format(byteutil.formatBytesMessage(bytesmsg[:-1])))

    try:
        sock.sendto(bytesmsg, dest_address)
    except Exception as e:
        if e.errno == 10051:  # Winerror 10051: unreachable network
            traceback.print_exc(limit=0)
        else:
            raise


def sendTCP(sock, bytesmsg):
    if SHOW_NET_INFO:
        print("┌ Sending TCP message via socket", reprTCPSocket(sock))
        print("│ ┌Message (bytes): '{}'".format(bytesmsg))
        print("└ └Message (print): {}".format(byteutil.formatBytesMessage(bytesmsg)))

    try:
        sock.sendall(bytesmsg)
    except Exception as e:
        if e.errno == 10051:  # Winerror 10051: unreachable network
            traceback.print_exc(limit=0)
        else:
            raise


def awaitUDP(sock, size):
    sock.settimeout(SOCK_TIMEOUT)
    bmsg, addr = sock.recvfrom(size)
    return (bmsg[:-1], addr)


def awaitTCP(sock, size):
    sock.settimeout(SOCK_TIMEOUT)
    return sock.recv(size)[:-1]


UDP_MSG_SIZE = 2**12
MSG_SIZE = 2**12

SERVER_IP = getOwnIP()  # Use machine IPv4 Address e.g. 192.168.1.1X
SERVER_UDP_PORT = 64
CLIENT_UDP_PORT = 65
SERVER_TCP_PORT = 66
SOCK_TIMEOUT = 1
SHOW_NET_INFO = False
