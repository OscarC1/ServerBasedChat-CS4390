# from Codes import Code
import byteutil
import traceback
import socket
# import timeout_decorator

MESSAGE_TERM = bytes(chr(3), 'utf-8')

def newUDPSocket():
    """Get a new UDP socket."""
    return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def newTCPSocket():
    """Get a new TCP socket."""
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def reprTCPSocket(sock):
    """Represent a TCP socket as a concise string.
    
    Args:
        sock : TCP socket
    
    Returns:
        str: Representation
    """
    closed = getattr(sock, '_closed', False)
    return "<{}{} --> {}>".format(
        "[closed] " if closed else "",
        sock.getsockname(),
        sock.getpeername()
    )


def reprSocketServer(sockserv):
    """Represent a socketserver as a concise string.
    
    Args:
        sockserv
    
    Returns:
        str: Representation
    """
    return "<(SocketServer listening on {sock})>".format(
        sock=sockserv.socket.getsockname()
    )


def getOwnIP():
    """Determine the best IP to listen/bind on.
    Returns some kind of object, probably.
    """
    return ''
    # for addrinfo in socket.getaddrinfo(socket.gethostname(), 0):
    #     family, __, __, __, address = addrinfo
    #         if family == socket.AddressFamily.AF_INET:
    #             return address[0]


def sendUDP(sock, bytesmsg, dest_address):
    """Takes a bytes-formatted message and sends it.
    Automatically packs the terminator.
    
    Args:
        sock: Sending socket
        bytesmsg (bytes): Bytes-formatted message, output of message2bytes
        dest_address: Destination socket address
    """
    if SHOW_NET_INFO:
        print("┌ Sending UDP message")
        print("│ Server: {}:{}".format(*dest_address))
        print("│ ┌Message (bytes): '{}'".format(bytesmsg))
        print("└ └Message (print): {}".format(byteutil.formatBytesMessage(bytesmsg[:-1])))

    try:
        sock.sendto(bytesmsg + MESSAGE_TERM, dest_address)
    except Exception as e:
        if e.errno == 10051:  # Winerror 10051: unreachable network
            traceback.print_exc(limit=0)
        else:
            raise


def sendTCP(sock, bytesmsg):
    """Takes a bytes-formatted message and sends it.
    Automatically packs the terminator.
    
    Args:
        sock: Sending socket
        bytesmsg (bytes): Bytes-formatted message, output of message2bytes
        dest_address: Destination socket address
    """
    if SHOW_NET_INFO:
        print("┌ Sending TCP message via socket", reprTCPSocket(sock))
        print("│ ┌Message (bytes): '{}'".format(bytesmsg))
        print("└ └Message (print): {}".format(byteutil.formatBytesMessage(bytesmsg)))

    try:
        sock.sendall(bytesmsg + MESSAGE_TERM)
    except Exception as e:
        if e.errno == 10051:  # Winerror 10051: unreachable network
            traceback.print_exc(limit=0)
        else:
            raise


def awaitUDP(sock, size):
    """Recieves a single message and returns it.
    This strips terminators.
    
    Args:
        sock (sock): Receiving UDP socket
        size (int): Packet size
    
    Returns:
        bytes: Response, without terminator.
    """
    sock.settimeout(SOCK_TIMEOUT)
    bmsg, addr = sock.recvfrom(size)
    return (bmsg[:-1], addr)


def awaitTCP(sock, size):
    """Recieves a single message and returns it.
    This strips terminators.
    
    Args:
        sock (sock): Receiving TCP socket
        size (int): Packet size
    
    Returns:
        bytes: Response, without terminator.
    """
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
